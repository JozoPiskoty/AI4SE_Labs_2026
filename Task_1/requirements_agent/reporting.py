from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PRIORITIES = {
    "P1": "Critical: necessary for basic operation, compliance, or a critical need.",
    "P2": "High: significant functionality or operational need.",
    "P3": "Medium: useful capability that meaningfully improves the system.",
    "P4": "Low: optional enhancement or requirement with lower impact.",
}


def _cell(value: Any) -> str:
    if isinstance(value, list):
        value = ", ".join(str(item) for item in value) if value else "—"
    if value is None or value == "":
        value = "—"
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def render_requirements(state: dict[str, Any], input_dir: Path) -> str:
    documents = state.get("manifest", [])
    requirements = state.get("requirements", [])
    coverage_notes = state.get("coverage_notes", [])
    by_source: dict[str, list[str]] = {item["id"]: [] for item in documents}
    for requirement in requirements:
        for source in requirement.get("source_documents", []):
            if source in by_source:
                by_source[source].append(requirement["id"])

    lines = [
        "# Software Requirements Specification",
        "",
        "## A. Document overview",
        "",
        "This document consolidates software requirements extracted from the supplied corpus. "
        "Requirements and priorities are model-generated and require stakeholder validation; "
        "unresolved conflicts and incomplete evidence are listed below.",
        "",
        f"- Input corpus: `{input_dir}`",
        f"- Documents discovered: {len(documents)}",
        f"- Requirements: {len(requirements)}",
        f"- Review repair iterations: {state.get('iterations', 0)}",
        "",
        "## B. Priority scale",
        "",
    ]
    lines.extend(f"- **{key}** — {value}" for key, value in PRIORITIES.items())
    lines.extend([
        "",
        "Priorities are estimates unless a requirement explicitly records source-based priority evidence. "
        "The per-requirement rationale and `priority_is_estimated` field identify this distinction.",
        "",
        "## C. Glossary",
        "",
        "No glossary terms were independently established by the network. Add stakeholder-approved "
        "definitions before baselining this specification.",
        "",
        "## D. Accepted requirements",
        "",
    ])
    if not requirements:
        lines.append("_No requirements were produced._")
    for item in requirements:
        lines.extend([
            f"### {item['id']}: {_cell(item.get('name'))}",
            "",
            f"- **Category:** {_cell(item.get('category'))}",
            f"- **Priority:** {_cell(item.get('priority'))}"
            + (" (estimated)" if item.get("priority_is_estimated", True) else " (source-supported)"),
            f"- **Priority rationale:** {_cell(item.get('priority_rationale'))}",
            f"- **Sources:** {_cell(item.get('source_documents'))}",
            f"- **Evidence:** {_cell(item.get('evidence'))}",
            f"- **Manual provenance review required:** {'Yes' if item.get('manual_review_required') else 'No'}",
            f"- **Confidence:** {_cell(item.get('confidence'))}",
            f"- **Related questions/dependencies:** {_cell(item.get('related_questions'))}",
            "",
            _cell(item.get("statement")),
            "",
        ])

    lines.extend(["## E. Blacklist of rejected candidates", ""])
    rejected = state.get("rejected", [])
    if not rejected:
        lines.append("_No rejected candidates were reported by the agents._")
    else:
        for item in rejected:
            lines.extend([
                f"### {item['id']}: {_cell(item.get('description'))}",
                "",
                f"- **Sources:** {_cell(item.get('source_documents'))}",
                f"- **Reason:** {_cell(item.get('reason'))}",
                f"- **Related requirements/evidence:** {_cell(item.get('related_requirements'))}",
                f"- **Human review required:** {'Yes' if item.get('human_review_required') else 'No'}",
                "",
            ])

    lines.extend([
        "## F. Source coverage and completeness",
        "",
        "| Source document | Status | Requirement IDs | Coverage note |",
        "|---|---|---|---|",
    ])
    for doc in documents:
        notes = [
            item["note"] for item in coverage_notes
            if item.get("source_document") == doc["id"]
        ]
        note = "; ".join(dict.fromkeys(notes)) or (
            "No requirement was traced to this document; this is not proof that it contains none."
            if not by_source[doc["id"]] else "Requirements were traced to this document."
        )
        lines.append(
            f"| {_cell(doc['name'])} | {_cell(doc['status'])} | "
            f"{_cell(by_source[doc['id']])} | {_cell(note)} |"
        )
    lines.extend(["", "### Processing warnings", ""])
    issues = state.get("issues", [])
    if issues:
        lines.extend(f"- **{_cell(item.get('document'))}:** {_cell(item.get('issue'))}" for item in issues)
    else:
        lines.append("_No corpus loading warnings._")
    validation_errors = state.get("validation_errors", [])
    if validation_errors:
        lines.extend(f"- **Validation:** {_cell(error)}" for error in validation_errors)
    validation_warnings = state.get("validation_warnings", [])
    if validation_warnings:
        lines.extend(f"- **Validation warning:** {_cell(warning)}" for warning in validation_warnings)
    findings = state.get("findings", [])
    if findings:
        lines.extend(f"- **Review finding:** {_cell(item.get('issue'))}" for item in findings)

    lines.extend(["", "## G. Unresolved questions", ""])
    questions = list(state.get("unresolved_questions", []))
    questions.extend(
        finding["issue"] for finding in findings
        if finding.get("repair_target") == "human"
    )
    questions = list(dict.fromkeys(questions))
    if questions:
        lines.extend(f"- {question}" for question in questions)
    else:
        lines.append("_No unresolved questions were returned by the review agent._")
    lines.append("")
    return "\n".join(lines)


def write_outputs(state: dict[str, Any], input_dir: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "requirements.md").write_text(
        render_requirements(state, input_dir), encoding="utf-8"
    )
    summary = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "input_dir": str(input_dir),
        "documents": state.get("manifest", []),
        "loading_issues": state.get("issues", []),
        "requirement_count": len(state.get("requirements", [])),
        "rejected_candidate_count": len(state.get("rejected", [])),
        "review_iterations": state.get("iterations", 0),
        "validation_errors": state.get("validation_errors", []),
        "validation_warnings": state.get("validation_warnings", []),
        "review_findings": state.get("findings", []),
    }
    (output_dir / "run_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )
