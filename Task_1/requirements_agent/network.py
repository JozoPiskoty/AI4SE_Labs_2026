from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Any, TypedDict

from langgraph.graph import END, START, StateGraph

from .cache import ConsolidationCache, ExtractionCache
from .corpus import batch_documents, load_corpus
from .models import ReviewResult
from .progress import safe_error_message, timed_invoke


LOGGER = logging.getLogger("requirements_agent")
EXTRACTION_PROMPT_VERSION = "1"
CONSOLIDATION_PROMPT_VERSION = "3"


class NetworkState(TypedDict, total=False):
    input_dir: str
    output_dir: str
    documents: list[dict[str, Any]]
    manifest: list[dict[str, Any]]
    issues: list[dict[str, str]]
    candidates: list[dict[str, Any]]
    requirements: list[dict[str, Any]]
    rejected: list[dict[str, Any]]
    unresolved_questions: list[str]
    coverage_notes: list[dict[str, str]]
    findings: list[dict[str, Any]]
    feedback: str
    iterations: int
    max_iterations: int
    consolidation_batch_size: int
    repair_requirement_ids: list[str]
    repair_candidate_refs: list[str]
    repair_performed: bool
    retry_allowed: bool
    validation_errors: list[str]
    validation_warnings: list[str]


def _dump(model: Any) -> dict[str, Any]:
    return model.model_dump() if hasattr(model, "model_dump") else model


def _unique(values: list[str]) -> list[str]:
    return list(dict.fromkeys(value for value in values if value))


def _unknown_sources(source_documents: list[str], valid_sources: set[str]) -> list[str]:
    return sorted(set(source_documents) - valid_sources)


def _resolve_candidate_sources(
    candidate: dict[str, Any],
    documents: list[dict[str, Any]],
    valid_sources: set[str],
) -> tuple[list[str], list[str]]:
    sources: list[str] = []
    unresolved_reference_count = 0
    loaded_documents = [
        document for document in documents
        if document.get("status") == "loaded" and document.get("id") in valid_sources
    ]
    candidate_references = candidate.get("source_documents", [])

    for reference in candidate_references:
        if reference in valid_sources:
            sources.append(reference)
            continue

        email_matches = {address.casefold() for address in re.findall(
            r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}",
            str(reference),
            flags=re.IGNORECASE,
        )}
        matching_headers = [
            document for document in loaded_documents
            if email_matches & {address.casefold() for address in re.findall(
                r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}",
                str(document.get("text", "")).split("\n\n", 1)[0],
                flags=re.IGNORECASE,
            )}
        ]
        if len(matching_headers) == 1:
            sources.append(matching_headers[0]["id"])
            continue

        unresolved_reference_count += 1

    if unresolved_reference_count or not sources:
        evidence = [
            " ".join(str(item).casefold().split())
            for item in candidate.get("evidence", [])
            if str(item).strip()
        ]
        evidence_matches: set[str] = set()
        for document in loaded_documents:
            text = " ".join(str(document.get("text", "")).casefold().split())
            if any(item in text for item in evidence):
                evidence_matches.add(document["id"])
        if len(evidence_matches) == 1:
            sources.extend(evidence_matches)
            if unresolved_reference_count <= 1:
                unresolved_reference_count = 0

    warnings = []
    if unresolved_reference_count or not sources:
        warnings.append(
            "One or more candidate source references could not be reliably mapped to an input document."
        )
    return _unique(sources), warnings


def _provenance_for_refs(
    refs: list[str],
    provenance: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    records = [provenance[ref] for ref in refs if ref in provenance]
    warnings = _unique([
        warning for record in records for warning in record.get("provenance_warnings", [])
    ])
    return {
        "source_documents": _unique([
            source for record in records for source in record.get("source_documents", [])
        ]),
        "evidence": _unique([
            evidence for record in records for evidence in record.get("evidence", [])
        ]),
        "manual_review_required": bool(warnings),
        "provenance_warnings": warnings,
    }


def build_graph(
    extraction_model: Any,
    consolidation_model: Any,
    review_model: Any,
    model_names: dict[str, str] | None = None,
    api_secret: str | None = None,
    extraction_batch_chars: int = 12000,
    consolidation_batch_size: int = 45,
):
    if extraction_batch_chars < 1:
        raise ValueError("extraction_batch_chars must be greater than zero")
    if consolidation_batch_size < 1:
        raise ValueError("consolidation_batch_size must be greater than zero")
    model_names = model_names or {
        "extraction": "extraction model",
        "consolidation": "consolidation model",
        "review": "review model",
    }

    def load_node(state: NetworkState) -> dict[str, Any]:
        LOGGER.info("Načítavam vstupné dokumenty z %s.", state["input_dir"])
        docs, issues = load_corpus(
            Path(state["input_dir"]),
            Path(state["output_dir"]),
        )
        LOGGER.info("Načítaných %d dokumentov.", len(docs))
        if issues:
            LOGGER.warning("Pri načítaní zaznamenaných problémov: %d.", len(issues))
        return {
            "documents": docs,
            "manifest": [{"id": d["id"], "name": d["name"], "status": d["status"]} for d in docs],
            "issues": issues,
            "iterations": 0,
            "candidates": [],
            "requirements": [],
            "rejected": [],
            "unresolved_questions": [],
            "repair_performed": False,
            "coverage_notes": [],
            "validation_errors": [],
            "validation_warnings": [],
        }

    def extract_node(state: NetworkState) -> dict[str, Any]:
        candidates: list[dict[str, Any]] = []
        rejected: list[dict[str, Any]] = []
        coverage: list[dict[str, str]] = []
        batches = batch_documents(state["documents"], max_chars=extraction_batch_chars)
        cache = ExtractionCache(Path(state["output_dir"]))
        LOGGER.info("Spúšťam agenta na extrakciu požiadaviek (%s).", model_names["extraction"])
        for batch_index, batch in enumerate(batches, start=1):
            LOGGER.info("Extrakcia: dávka %d/%d.", batch_index, len(batches))
            feedback = state.get("feedback", "None")
            result = cache.get(
                model_names["extraction"],
                EXTRACTION_PROMPT_VERSION,
                batch,
                feedback,
            )
            if result is not None:
                LOGGER.info(
                    "Používam uložený výsledok extrakcie pre dávku %d/%d.",
                    batch_index,
                    len(batches),
                )
            else:
                docs_json = json.dumps(
                    [{"name": d["name"], "text": d["text"]} for d in batch],
                    ensure_ascii=False,
                )
                prompt = (
                    "Extract atomic, evidence-supported software requirements from these source documents. "
                    "Ignore personal remarks and irrelevant discussion. Preserve conditions and exceptions. "
                    "Do not invent facts. Distinguish uncertain inferences and explicit priority evidence. "
                    "Every source reference must exactly match one of the supplied names. Record notable "
                    "non-requirement candidates only when they could be mistaken for requirements.\n"
                    f"REVIEW FEEDBACK TO ADDRESS:\n{feedback}\n\n"
                    f"SOURCE DOCUMENTS:\n{docs_json}"
                )
                try:
                    result = timed_invoke(
                        extraction_model,
                        prompt,
                        node="extrakcia",
                        model_name=model_names["extraction"],
                        batch=f"dávka {batch_index}/{len(batches)}",
                        secret=api_secret,
                    )
                except Exception as exc:
                    LOGGER.error(
                        "Extrakčná dávka %d/%d definitívne zlyhala; úspešné dávky zostávajú v cache (%s: %s).",
                        batch_index,
                        len(batches),
                        type(exc).__name__,
                        safe_error_message(exc, api_secret),
                    )
                    raise
                cache.put(
                    model_names["extraction"],
                    EXTRACTION_PROMPT_VERSION,
                    batch,
                    result,
                    feedback,
                )
                LOGGER.info(
                    "Uložený výsledok extrakcie pre dávku %d/%d do lokálnej cache.",
                    batch_index,
                    len(batches),
                )
            candidates.extend(_dump(item) for item in result.candidates)
            rejected.extend(_dump(item) for item in result.rejected)
            coverage.extend(_dump(item) for item in result.coverage_notes)
        LOGGER.info(
            "Extrakcia dokončená: %d kandidátov, %d zamietnutých kandidátov.",
            len(candidates),
            len(rejected),
        )
        return {
            "candidates": candidates,
            "rejected": state.get("rejected", []) + rejected,
            "coverage_notes": state.get("coverage_notes", []) + coverage,
        }

    def consolidate_node(state: NetworkState) -> dict[str, Any]:
        LOGGER.info("Spúšťam jednopriechodovú konsolidáciu (%s).", model_names["consolidation"])
        cache = ConsolidationCache(Path(state["output_dir"]))
        batch_size = state.get("consolidation_batch_size", consolidation_batch_size)
        feedback = state.get("feedback", "None")
        manifest_names = [item["id"] for item in state.get("manifest", [])]
        valid_sources = set(manifest_names)
        documents = state.get("documents", [])
        candidates: list[dict[str, Any]] = []
        cache_candidates: list[dict[str, Any]] = []
        provenance: dict[str, dict[str, Any]] = {}
        for index, candidate in enumerate(state.get("candidates", []), start=1):
            cache_item = dict(candidate)
            item = dict(candidate)
            ref = f"CAND-{index:06d}"
            cache_item["candidate_refs"] = [ref]
            resolved_sources, provenance_warnings = _resolve_candidate_sources(
                item, documents, valid_sources
            )
            item["source_documents"] = resolved_sources
            item["provenance_warnings"] = provenance_warnings
            item["manual_review_required"] = bool(provenance_warnings)
            item["_cache_repair_source_documents"] = list(candidate.get("source_documents", []))
            item["_cache_repair_evidence"] = list(candidate.get("evidence", []))
            item["candidate_refs"] = [ref]
            candidates.append(item)
            cache_candidates.append(cache_item)
            provenance[ref] = {
                "source_documents": resolved_sources,
                "evidence": list(item.get("evidence", [])),
                "provenance_warnings": provenance_warnings,
                "cache_source_documents": list(candidate.get("source_documents", [])),
                "cache_evidence": list(candidate.get("evidence", [])),
            }

        rejected: list[dict[str, Any]] = []
        for rejected_item in state.get("rejected", []):
            item = dict(rejected_item)
            resolved_sources, provenance_warnings = _resolve_candidate_sources(
                item, documents, valid_sources
            )
            item["source_documents"] = resolved_sources
            item["provenance_warnings"] = provenance_warnings
            item["manual_review_required"] = bool(provenance_warnings)
            rejected.append(item)

        groups = [candidates[start:start + batch_size] for start in range(0, len(candidates), batch_size)]
        cache_groups = [
            cache_candidates[start:start + batch_size]
            for start in range(0, len(cache_candidates), batch_size)
        ]
        requirements: list[dict[str, Any]] = []
        questions: list[str] = list(state.get("unresolved_questions", []))
        for group_index, group in enumerate(groups, start=1):
            cache_group = cache_groups[group_index - 1]
            context = json.dumps({
                "phase": "single-pass-local-consolidation",
                "group": group_index,
                "group_count": len(groups),
                "batch_size": batch_size,
                "manifest": manifest_names,
                "feedback": feedback,
            }, ensure_ascii=False, sort_keys=True)
            prompt_group = [
                {key: value for key, value in candidate.items() if not key.startswith("_cache_")}
                for candidate in group
            ]
            result = cache.get(
                model_names["consolidation"], CONSOLIDATION_PROMPT_VERSION, cache_group, context
            )
            if result is None:
                prompt = (
                    "Consolidate this one bounded group of software requirement candidates. Merge only "
                    "true semantic duplicates with the same scope, conditions and exceptions; keep every "
                    "independent requirement. Normalize terminology. Preserve priorities and explain them. "
                    "For every accepted requirement include all candidate_refs it represents. For each "
                    "rejected candidate include its candidate_refs and a reason. Never invent references. "
                    "Preserve every source and evidence item. Record unresolved conflicts as questions. "
                    "Apply the targeted feedback only to candidates explicitly named in it.\n"
                    f"FEEDBACK: {feedback}\n"
                    f"KNOWN SOURCES: {json.dumps(manifest_names, ensure_ascii=False)}\n"
                    f"GROUP {group_index}/{len(groups)} ({len(group)} candidates):\n"
                    f"{json.dumps(prompt_group, ensure_ascii=False)}"
                )
                LOGGER.info(
                    "Konsolidácia: skupina %d/%d (%d kandidátov).",
                    group_index, len(groups), len(group),
                )
                try:
                    result = timed_invoke(
                        consolidation_model, prompt,
                        node=f"konsolidácia skupina {group_index}/{len(groups)}",
                        model_name=model_names["consolidation"],
                        batch=f"skupina {group_index}/{len(groups)}",
                        secret=api_secret,
                    )
                except Exception as exc:
                    LOGGER.error(
                        "Konsolidácia zlyhala: fáza local, model %s, skupina %d/%d (%s: %s).",
                        model_names["consolidation"], group_index, len(groups),
                        type(exc).__name__, safe_error_message(exc, api_secret),
                    )
                    raise
                cache.put(
                    model_names["consolidation"], CONSOLIDATION_PROMPT_VERSION,
                    cache_group, context, result,
                )
            else:
                LOGGER.info("Načítavam konsolidáciu skupiny %d/%d z cache.", group_index, len(groups))

            questions.extend(result.unresolved_questions)
            valid_refs = {ref for item in group for ref in item["candidate_refs"]}
            covered_refs: set[str] = set()
            group_requirements: list[dict[str, Any]] = []
            for requirement in result.requirements:
                item = _dump(requirement)
                refs = list(dict.fromkeys(ref for ref in item.get("candidate_refs", []) if ref in valid_refs))
                covered_refs.update(refs)
                item["candidate_refs"] = refs
                item["_cache_repair_source_documents"] = _unique(
                    list(item.get("source_documents", []))
                    + [source for ref in refs for source in provenance[ref]["cache_source_documents"]]
                )
                item["_cache_repair_evidence"] = _unique(
                    list(item.get("evidence", []))
                    + [evidence for ref in refs for evidence in provenance[ref]["cache_evidence"]]
                )
                item.update(_provenance_for_refs(refs, provenance))
                group_requirements.append(item)
            for rejected_candidate in result.rejected:
                item = _dump(rejected_candidate)
                refs = list(dict.fromkeys(ref for ref in item.get("candidate_refs", []) if ref in valid_refs))
                covered_refs.update(refs)
                item["candidate_refs"] = refs
                item.update(_provenance_for_refs(refs, provenance))
                rejected.append(item)

            for candidate in group:
                missing = [ref for ref in candidate["candidate_refs"] if ref not in covered_refs]
                if missing:
                    fallback = dict(candidate)
                    fallback["candidate_refs"] = missing
                    fallback["related_questions"] = []
                    group_requirements.append(fallback)
                    LOGGER.warning(
                        "Konsolidácia skupiny %d/%d nevrátila %d kandidátov; zachovávam ich.",
                        group_index, len(groups), len(missing),
                    )
            for item in group_requirements:
                item["origin_groups"] = [group_index]
                requirements.append(item)

        for index, requirement in enumerate(requirements, start=1):
            requirement["draft_id"] = f"DREQ-{index:04d}"
        LOGGER.info(
            "Jednopriechodová konsolidácia dokončená: %d kandidátov -> %d požiadaviek v %d skupinách.",
            len(candidates), len(requirements), len(groups),
        )
        return {
            "candidates": candidates,
            "requirements": requirements,
            "rejected": rejected,
            "unresolved_questions": list(dict.fromkeys(questions)),
        }

    def review_node(state: NetworkState) -> dict[str, Any]:
        LOGGER.info("Spúšťam globálnu kontrolu úplnosti a duplicít (%s).", model_names["review"])
        candidate_index = [
            {
                "candidate_ref": item["candidate_refs"][0],
                "name": item.get("name", "")[:120],
                "category": item.get("category", ""),
                "statement": item.get("statement", "")[:320],
                "source_documents": item.get("source_documents", []),
                "evidence": item.get("evidence", [])[:2],
            }
            for item in state.get("candidates", [])
        ]
        requirement_index = [
            {
                "requirement_id": item["draft_id"],
                "origin_groups": item.get("origin_groups", []),
                "name": item.get("name", "")[:120],
                "category": item.get("category", ""),
                "statement": item.get("statement", "")[:400],
                "source_documents": item.get("source_documents", []),
                "evidence": item.get("evidence", [])[:2],
                "candidate_refs": item.get("candidate_refs", []),
            }
            for item in state.get("requirements", [])
        ]
        prompt = (
            "Perform one global quality and completeness audit. Compare every extracted candidate with "
            "the consolidated requirements; check source coverage, unsupported content, contradictory "
            "requirements, and semantic duplicates, especially across different origin_groups. Do not "
            "request source documents: use the provided evidence and source IDs. Return duplicate_groups "
            "with requirement_ids for cross-group duplicates. For each repairable issue set repair_target "
            "and exact affected_requirement_ids and/or affected_candidate_refs. Use human when evidence is "
            "insufficient. Do not approve by default. The complete candidate index is the baseline for "
            "completeness; candidate_refs show traceability.\n"
            f"SOURCE MANIFEST: {json.dumps(state.get('manifest', []), ensure_ascii=False)}\n"
            f"EXTRACTION COVERAGE NOTES: {json.dumps(state.get('coverage_notes', []), ensure_ascii=False)}\n"
            f"CANDIDATE INDEX: {json.dumps(candidate_index, ensure_ascii=False)}\n"
            f"CONSOLIDATED REQUIREMENT INDEX: {json.dumps(requirement_index, ensure_ascii=False)}\n"
            f"EXISTING WARNINGS: {json.dumps(state.get('unresolved_questions', []), ensure_ascii=False)}"
        )
        result: ReviewResult = timed_invoke(
            review_model, prompt, node="globálna kontrola", model_name=model_names["review"],
            secret=api_secret,
        )
        findings = [_dump(item) for item in result.findings]
        repair_ids: set[str] = set()
        repair_refs: set[str] = set()
        req_ids = {item["draft_id"] for item in state.get("requirements", [])}
        cand_refs = {item["candidate_refs"][0] for item in state.get("candidates", [])}
        for finding in findings:
            if finding.get("repair_target") in {"extract", "consolidate"}:
                repair_ids.update(set(finding.get("affected_requirement_ids", [])) & req_ids)
                repair_refs.update(set(finding.get("affected_candidate_refs", [])) & cand_refs)
        for duplicate in result.duplicate_groups:
            duplicate_data = _dump(duplicate)
            ids = sorted(set(duplicate_data["requirement_ids"]) & req_ids)
            if len(ids) > 1:
                repair_ids.update(ids)
                findings.append({
                    "issue": duplicate_data["rationale"],
                    "repair_target": "consolidate",
                    "evidence": duplicate_data.get("evidence", []),
                    "affected_requirement_ids": ids,
                    "affected_candidate_refs": [],
                })
        if result.missing_requirements:
            missing_refs = set()
            for missing in result.missing_requirements:
                missing_refs.update(set(missing.candidate_refs) & cand_refs)
            if missing_refs:
                repair_refs.update(missing_refs)
                findings.append({
                    "issue": "Kontrola našla kandidátov, ktorí nie sú pokrytí požiadavkami.",
                    "repair_target": "consolidate",
                    "evidence": [],
                    "affected_requirement_ids": [],
                    "affected_candidate_refs": sorted(missing_refs),
                })
            else:
                LOGGER.warning("Kontrolný agent uviedol chýbajúce požiadavky bez platných candidate_refs.")
        unresolved = list(state.get("unresolved_questions", [])) + result.unresolved_questions
        actionable = bool(repair_ids or repair_refs)
        repair_available = not state.get("repair_performed", False) and state.get("max_iterations", 1) > 0
        if actionable and repair_available:
            LOGGER.info(
                "Kontrola našla cielené opravy: %d požiadaviek, %d kandidátov.",
                len(repair_ids), len(repair_refs),
            )
        elif actionable:
            unresolved.append("Opraviteľné nedostatky zostali po jedinom opravnom priechode; vyžadujú ľudskú kontrolu.")
        for finding in findings:
            if finding.get("repair_target") in {"extract", "consolidate"} and not (
                finding.get("affected_requirement_ids") or finding.get("affected_candidate_refs")
            ):
                unresolved.append(finding["issue"])
        if result.duplicate_groups and not (actionable and repair_available):
            unresolved.append("Po globálnej kontrole zostávajú možné sémantické duplicity na ľudské posúdenie.")
        return {
            "findings": findings,
            "feedback": "\n".join(item.get("issue", "") for item in findings),
            "repair_requirement_ids": sorted(repair_ids),
            "repair_candidate_refs": sorted(repair_refs),
            "retry_allowed": actionable and repair_available,
            "unresolved_questions": list(dict.fromkeys(unresolved)),
            "coverage_notes": state.get("coverage_notes", []) + [_dump(item) for item in result.coverage_notes],
            "rejected": state.get("rejected", []) + [_dump(item) for item in result.rejected],
        }

    def repair_node(state: NetworkState) -> dict[str, Any]:
        target_ids = set(state.get("repair_requirement_ids", []))
        target_refs = set(state.get("repair_candidate_refs", []))
        current = state.get("requirements", [])
        candidates = state.get("candidates", [])
        selected_requirements = [item for item in current if item.get("draft_id") in target_ids]
        represented_refs = {
            ref for item in selected_requirements for ref in item.get("candidate_refs", [])
        }
        missing_refs = target_refs - represented_refs
        selected_candidates = [
            item for item in candidates
            if item.get("candidate_refs", [None])[0] in missing_refs
        ]
        repair_inputs = [dict(item) for item in selected_requirements + selected_candidates]
        if not repair_inputs:
            LOGGER.warning("Cielený opravný priechod nemá platné ciele; zachovávam pôvodné výsledky.")
            return {"repair_performed": True, "iterations": 1, "retry_allowed": False}

        LOGGER.info("Spúšťam jediný cielený opravný priechod pre %d položiek.", len(repair_inputs))
        cache = ConsolidationCache(Path(state["output_dir"]))
        provenance = {
            ref: {
                "source_documents": item.get("source_documents", []),
                "evidence": item.get("evidence", []),
                "provenance_warnings": item.get("provenance_warnings", []),
            }
            for item in candidates
            for ref in item.get("candidate_refs", [])
        }
        ref_to_draft_id = {
            ref: item["draft_id"]
            for item in selected_requirements
            for ref in item.get("candidate_refs", [])
        }
        groups = [
            repair_inputs[start:start + consolidation_batch_size]
            for start in range(0, len(repair_inputs), consolidation_batch_size)
        ]
        cache_groups = []
        prompt_groups = []
        for group in groups:
            cache_group: list[dict[str, Any]] = []
            prompt_group: list[dict[str, Any]] = []
            for source in group:
                cache_item = {
                    key: value for key, value in source.items()
                    if not key.startswith("_cache_")
                    and key not in {"manual_review_required", "provenance_warnings"}
                }
                if "_cache_repair_source_documents" in source:
                    cache_item["source_documents"] = source["_cache_repair_source_documents"]
                if "_cache_repair_evidence" in source:
                    cache_item["evidence"] = source["_cache_repair_evidence"]
                cache_group.append(cache_item)
                prompt_group.append({
                    key: value for key, value in source.items()
                    if not key.startswith("_cache_")
                })
            cache_groups.append(cache_group)
            prompt_groups.append(prompt_group)
        replacements: list[dict[str, Any]] = []
        rejected: list[dict[str, Any]] = []
        questions: list[str] = []
        for group_index, group in enumerate(groups, start=1):
            cache_group = cache_groups[group_index - 1]
            prompt_group = prompt_groups[group_index - 1]
            context = json.dumps({
                "phase": "single-targeted-repair",
                "group": group_index,
                "feedback": state.get("feedback", ""),
                "manifest": [item["id"] for item in state.get("manifest", [])],
            }, ensure_ascii=False, sort_keys=True)
            result = cache.get(
                model_names["consolidation"],
                CONSOLIDATION_PROMPT_VERSION,
                cache_group,
                context,
            )
            if result is None:
                prompt = (
                    "Repair only the supplied flagged requirements/candidates. Do not reprocess other "
                    "requirements. Merge only true semantic duplicates, preserve distinct obligations, "
                    "conditions and exceptions, and include every represented candidate_ref. Preserve all "
                    "source_documents and evidence. Keep rejected candidates and reasons. Return the full "
                    "corrected result for these inputs.\n"
                    f"REVIEW FEEDBACK: {state.get('feedback', '')}\n"
                    f"TARGETED INPUTS: {json.dumps(prompt_group, ensure_ascii=False)}"
                )
                try:
                    result = timed_invoke(
                        consolidation_model, prompt, node=f"cielená oprava skupina {group_index}/{len(groups)}",
                        model_name=model_names["consolidation"], batch=f"skupina {group_index}/{len(groups)}",
                        secret=api_secret,
                    )
                except Exception as exc:
                    LOGGER.error(
                        "Cielená oprava zlyhala: fáza repair, model %s, skupina %d/%d (%s: %s).",
                        model_names["consolidation"], group_index, len(groups), type(exc).__name__,
                        safe_error_message(exc, api_secret),
                    )
                    raise
                cache.put(
                    model_names["consolidation"],
                    CONSOLIDATION_PROMPT_VERSION,
                    cache_group,
                    context,
                    result,
                )
            questions.extend(result.unresolved_questions)
            valid_refs = {ref for item in group for ref in item.get("candidate_refs", [])}
            covered: set[str] = set()
            for item_model in result.requirements:
                item = _dump(item_model)
                refs = list(dict.fromkeys(ref for ref in item.get("candidate_refs", []) if ref in valid_refs))
                covered.update(refs)
                item["candidate_refs"] = refs
                item["origin_groups"] = list(dict.fromkeys(
                    origin for source in group if set(refs) & set(source.get("candidate_refs", []))
                    for origin in source.get("origin_groups", [])
                ))
                item.update(_provenance_for_refs(refs, provenance))
                replacements.append(item)
            for rejected_model in result.rejected:
                item = _dump(rejected_model)
                refs = list(dict.fromkeys(ref for ref in item.get("candidate_refs", []) if ref in valid_refs))
                covered.update(refs)
                item["candidate_refs"] = refs
                item.update(_provenance_for_refs(refs, provenance))
                rejected.append(item)
            for source in group:
                missing = set(source.get("candidate_refs", [])) - covered
                if missing:
                    fallback = dict(source)
                    fallback["candidate_refs"] = sorted(missing)
                    replacements.append(fallback)
                    covered.update(missing)

        replaced_ids = {item["draft_id"] for item in selected_requirements}
        remaining = [item for item in current if item.get("draft_id") not in replaced_ids]
        used_ids = {item.get("draft_id") for item in remaining}
        numeric_ids = [
            int(identifier.removeprefix("DREQ-"))
            for identifier in (item.get("draft_id", "") for item in current)
            if identifier.startswith("DREQ-") and identifier[5:].isdigit()
        ]
        next_id = max(numeric_ids, default=0) + 1
        for item in replacements:
            preserved_id = next((
                ref_to_draft_id[ref]
                for ref in item.get("candidate_refs", [])
                if ref in ref_to_draft_id and ref_to_draft_id[ref] not in used_ids
            ), None)
            if preserved_id is None:
                preserved_id = f"DREQ-{next_id:04d}"
                next_id += 1
            item["draft_id"] = preserved_id
            used_ids.add(preserved_id)
        LOGGER.info("Cielený opravný priechod dokončený; spracovaných %d položiek.", len(repair_inputs))
        return {
            "requirements": remaining + replacements,
            "rejected": state.get("rejected", []) + rejected,
            "unresolved_questions": list(dict.fromkeys(state.get("unresolved_questions", []) + questions)),
            "repair_performed": True,
            "iterations": 1,
            "retry_allowed": False,
        }

    def route_after_review(state: NetworkState) -> str:
        if state.get("retry_allowed", False) and not state.get("repair_performed", False):
            return "repair"
        return "validate"

    def validate_node(state: NetworkState) -> dict[str, Any]:
        LOGGER.info("Validujem výsledné požiadavky a zdrojové odkazy.")
        valid_sources = {item["id"] for item in state.get("manifest", [])}
        errors: list[str] = []
        warnings: list[str] = []
        unresolved = list(state.get("unresolved_questions", []))
        finalized: list[dict[str, Any]] = []
        assigned_ids: set[str] = set()
        for index, requirement in enumerate(state.get("requirements", []), start=1):
            item = dict(requirement)
            item.pop("provenance_warnings", None)
            for key in [key for key in item if key.startswith("_cache_")]:
                item.pop(key)
            item.pop("candidate_refs", None)
            draft_id = item.pop("draft_id", "")
            item.pop("origin_groups", None)
            provenance_warnings = requirement.get("provenance_warnings", [])
            for warning in provenance_warnings:
                message = f"Requirement candidate {index}: {warning}"
                warnings.append(message)
                unresolved.append(message)
            if requirement.get("manual_review_required") and not item.get("source_documents"):
                warnings.append(
                    f"Requirement candidate {index} has no reliably mapped source document; manual review is required."
                )
                item["manual_review_required"] = True
            missing_fields = [
                key for key in ("name", "category", "statement", "priority", "priority_rationale", "source_documents")
                if not item.get(key)
            ]
            if requirement.get("manual_review_required"):
                missing_fields = [key for key in missing_fields if key != "source_documents"]
            if missing_fields:
                errors.append(f"Requirement candidate {index} is missing: {', '.join(missing_fields)}.")
            if item.get("priority") not in {"P1", "P2", "P3", "P4"}:
                errors.append(f"Requirement candidate {index} has invalid priority {item.get('priority')!r}.")
            unknown = _unknown_sources(item.get("source_documents", []), valid_sources)
            if unknown:
                errors.append(f"Requirement candidate {index} references unknown source(s): {', '.join(unknown)}.")
            draft_number = (
                int(draft_id[5:])
                if isinstance(draft_id, str) and draft_id.startswith("DREQ-") and draft_id[5:].isdigit()
                else index
            )
            final_id = f"REQ-{draft_number:03d}"
            while final_id in assigned_ids:
                draft_number += 1
                final_id = f"REQ-{draft_number:03d}"
            assigned_ids.add(final_id)
            item["id"] = final_id
            finalized.append(item)

        unique_rejected: list[dict[str, Any]] = []
        seen_rejected: set[tuple[str, str, tuple[str, ...]]] = set()
        for item in state.get("rejected", []):
            key = (
                " ".join(str(item.get("description", "")).casefold().split()),
                " ".join(str(item.get("reason", "")).casefold().split()),
                tuple(sorted(item.get("source_documents", []))),
            )
            if key not in seen_rejected:
                seen_rejected.add(key)
                unique_rejected.append(item)
        finalized_rejected = []
        for index, item in enumerate(unique_rejected, start=1):
            if not item.get("description") or not item.get("reason"):
                errors.append(f"Rejected candidate {index} is missing description or reason.")
            item = dict(item)
            for warning in item.pop("provenance_warnings", []):
                message = f"Rejected candidate {index}: {warning}"
                warnings.append(message)
                unresolved.append(message)
            item["id"] = f"BL-{index:03d}"
            unknown = _unknown_sources(item.get("source_documents", []), valid_sources)
            if unknown:
                errors.append(f"Blacklist candidate {index} references unknown source(s): {', '.join(unknown)}.")
            finalized_rejected.append(item)
        if errors:
            LOGGER.warning("Validácia dokončená s %d upozorneniami.", len(errors))
        else:
            LOGGER.info("Validácia dokončená bez chýb.")
        return {
            "requirements": finalized,
            "rejected": finalized_rejected,
            "validation_errors": errors,
            "validation_warnings": list(dict.fromkeys(
                state.get("validation_warnings", []) + warnings
            )),
            "unresolved_questions": list(dict.fromkeys(unresolved)),
        }

    graph = StateGraph(NetworkState)
    graph.add_node("load", load_node)
    graph.add_node("extract", extract_node)
    graph.add_node("consolidate", consolidate_node)
    graph.add_node("review", review_node)
    graph.add_node("repair", repair_node)
    graph.add_node("validate", validate_node)
    graph.add_edge(START, "load")
    graph.add_edge("load", "extract")
    graph.add_edge("extract", "consolidate")
    graph.add_edge("consolidate", "review")
    graph.add_conditional_edges(
        "review",
        route_after_review,
        {"repair": "repair", "validate": "validate"},
    )
    graph.add_edge("repair", "review")
    graph.add_edge("validate", END)
    return graph.compile()
