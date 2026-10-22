import json
import tempfile
import time
import unittest
from pathlib import Path

from requirements_agent.cache import ConsolidationCache, ExtractionCache
from requirements_agent.corpus import batch_documents, load_corpus
from requirements_agent.models import (
    CandidateRequirement,
    ConsolidatedRequirement,
    ConsolidationResult,
    DuplicateGroup,
    ExtractionResult,
    RejectedCandidate,
    ReviewFinding,
    ReviewResult,
)
from requirements_agent.network import _unknown_sources, build_graph
from requirements_agent.progress import timed_invoke
from requirements_agent.reporting import write_outputs


class FakeModel:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def invoke(self, prompt):
        self.calls.append(prompt)
        response = self.responses.pop(0)
        if isinstance(response, Exception):
            raise response
        return response


class EchoConsolidator:
    def __init__(self):
        self.calls = []

    def invoke(self, prompt):
        self.calls.append(prompt)
        start = prompt.index("BOUNDED INPUT GROUP")
        items = json.loads(prompt[prompt.index("\n", start) + 1:])
        return ConsolidationResult(requirements=[
            ConsolidatedRequirement(**item)
            for item in items
        ])


class MergeEachGroupConsolidator:
    def __init__(self):
        self.calls = []

    def invoke(self, prompt):
        self.calls.append(prompt)
        start = prompt.index("BOUNDED INPUT GROUP")
        items = json.loads(prompt[prompt.index("\n", start) + 1:])
        refs = list(dict.fromkeys(
            ref for item in items for ref in item.get("candidate_refs", [])
        ))
        first = dict(items[0])
        first["name"] = "Grouped requirements"
        first["statement"] = "The system shall satisfy all requirements in the source group."
        first["candidate_refs"] = refs
        first["source_documents"] = list(dict.fromkeys(
            source for item in items for source in item.get("source_documents", [])
        ))
        first["evidence"] = list(dict.fromkeys(
            evidence for item in items for evidence in item.get("evidence", [])
        ))
        return ConsolidationResult(requirements=[ConsolidatedRequirement(**first)])


class CorpusTests(unittest.TestCase):
    def test_loads_text_and_email_and_excludes_output_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "input"
            (root / "nested").mkdir(parents=True)
            out = root / "generated"
            out.mkdir()
            (root / "notes.txt").write_text("Requirement text", encoding="utf-8")
            (root / "nested" / "mail.eml").write_text(
                "From: a@example.org\nSubject: Report\n\nNeed a report.\n",
                encoding="utf-8",
            )
            (out / "requirements.md").write_text("not an input", encoding="utf-8")
            docs, issues = load_corpus(root, out)
            self.assertEqual([doc["name"] for doc in docs], ["nested/mail.eml", "notes.txt"])
            self.assertIn("Subject: Report", docs[0]["text"])
            self.assertEqual(issues, [])

    def test_empty_files_are_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "empty.txt").write_text("", encoding="utf-8")
            docs, issues = load_corpus(root)
            self.assertEqual(docs[0]["status"], "empty")
            self.assertTrue(issues)

    def test_large_document_is_split_below_batch_limit(self):
        docs = [{"id": "large.txt", "name": "large.txt", "status": "loaded", "text": "x" * 70000}]
        batches = batch_documents(docs, max_chars=10000)
        self.assertGreater(len(batches), 1)
        self.assertTrue(all(len(batch[0]["text"]) <= 10000 for batch in batches))
        self.assertEqual("".join(item[0]["text"] for item in batches), docs[0]["text"])


class NetworkTests(unittest.TestCase):
    @staticmethod
    def _consolidation_candidates():
        return [
            CandidateRequirement(
                name=f"Requirement {index}",
                category="Functional",
                statement=f"The system shall perform action {index}.",
                priority="P3",
                priority_rationale="Estimated.",
                source_documents=[f"source-{index}.txt"],
                evidence=[f"Evidence for action {index}."],
            )
            for index in range(1, 5)
        ]

    @staticmethod
    def _consolidated(candidate, candidate_ref):
        return ConsolidatedRequirement(
            **candidate.model_dump(exclude={"candidate_refs"}),
            candidate_refs=[candidate_ref],
        )

    def _consolidation_app(self, extraction, consolidation, review):
        return build_graph(
            extraction,
            consolidation,
            review,
            model_names={
                "extraction": "extract-model",
                "consolidation": "consolidate-model",
                "review": "review-model",
            },
            consolidation_batch_size=2,
        )

    def test_consolidation_cache_invalidates_on_model_prompt_data_and_context(self):
        with tempfile.TemporaryDirectory() as directory:
            cache = ConsolidationCache(Path(directory))
            candidates = [{"name": "Requirement", "candidate_refs": ["CAND-1"]}]
            result = ConsolidationResult()
            cache.put("model-a", "prompt-v1", candidates, "stage 1", result)
            self.assertIsNotNone(cache.get("model-a", "prompt-v1", candidates, "stage 1"))
            self.assertIsNone(cache.get("model-b", "prompt-v1", candidates, "stage 1"))
            self.assertIsNone(cache.get("model-a", "prompt-v2", candidates, "stage 1"))
            self.assertIsNone(cache.get("model-a", "prompt-v1", candidates, "stage 2"))
            self.assertIsNone(cache.get(
                "model-a", "prompt-v1", [{"name": "Changed"}], "stage 1"
            ))
            self.assertNotIn("OPENAI_API_KEY", cache.path.read_text(encoding="utf-8"))

    def test_single_pass_checks_cross_group_duplicates_and_repairs_only_targets(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "input"
            output = Path(directory) / "output"
            root.mkdir()
            candidates = self._consolidation_candidates() + [
                CandidateRequirement(
                    name=f"Requirement {index}",
                    category="Functional",
                    statement=f"The system shall perform action {index}.",
                    priority="P3",
                    priority_rationale="Estimated.",
                    source_documents=[f"source-{index}.txt"],
                    evidence=[f"Evidence for action {index}."],
                )
                for index in (5, 6)
            ]
            for index in range(1, 7):
                (root / f"source-{index}.txt").write_text(f"Source {index}", encoding="utf-8")

            local_results = []
            for group_index in range(3):
                base = candidates[group_index * 2]
                local_results.append(ConsolidationResult(requirements=[
                    ConsolidatedRequirement(
                        **base.model_dump(exclude={"candidate_refs"}),
                        candidate_refs=[f"CAND-{group_index * 2 + 1:06d}", f"CAND-{group_index * 2 + 2:06d}"],
                    )
                ]))
            merged = ConsolidatedRequirement(
                name="Shared capability",
                category="Functional",
                statement="The system shall provide the shared capability.",
                priority="P2",
                priority_rationale="Supported by both source groups.",
                source_documents=[],
                evidence=[],
                candidate_refs=["CAND-000001", "CAND-000002", "CAND-000003", "CAND-000004"],
            )
            consolidator = FakeModel(local_results + [ConsolidationResult(requirements=[merged])])
            reviewer = FakeModel([
                ReviewResult(
                    approved=False,
                    duplicate_groups=[DuplicateGroup(
                        requirement_ids=["DREQ-0001", "DREQ-0002"],
                        rationale="These requirements describe the same capability across groups.",
                        evidence=["Matching scope and behavior."],
                    )],
                ),
                ReviewResult(approved=True),
            ])
            app = self._consolidation_app(
                FakeModel([ExtractionResult(candidates=candidates)]), consolidator, reviewer
            )
            state = app.invoke({
                "input_dir": str(root),
                "output_dir": str(output),
                "max_iterations": 1,
                "consolidation_batch_size": 2,
            })

            self.assertEqual(len(consolidator.calls), 4)
            self.assertEqual(len(reviewer.calls), 2)
            repair_prompt = consolidator.calls[-1]
            self.assertIn("CAND-000001", repair_prompt)
            self.assertIn("CAND-000004", repair_prompt)
            self.assertNotIn("CAND-000005", repair_prompt)
            self.assertNotIn("CAND-000006", repair_prompt)
            self.assertEqual(state["iterations"], 1)
            self.assertEqual(len(state["requirements"]), 2)
            by_statement = {item["statement"]: item for item in state["requirements"]}
            merged_output = by_statement["The system shall provide the shared capability."]
            self.assertEqual(
                set(merged_output["source_documents"]),
                {"source-1.txt", "source-2.txt", "source-3.txt", "source-4.txt"},
            )
            self.assertEqual(
                set(merged_output["evidence"]),
                {f"Evidence for action {index}." for index in range(1, 5)},
            )
            untouched = by_statement["The system shall perform action 5."]
            self.assertEqual(set(untouched["source_documents"]), {"source-5.txt", "source-6.txt"})

    def test_cross_group_duplicates_are_checked_in_one_global_review_call(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "input"
            root.mkdir()
            (root / "a.txt").write_text("Source A", encoding="utf-8")
            (root / "b.txt").write_text("Source B", encoding="utf-8")
            candidates = [
                candidate.model_copy(update={"source_documents": [source_name]})
                for candidate, source_name in zip(
                    self._consolidation_candidates()[:2],
                    ("a.txt", "b.txt"),
                )
            ]
            first = ConsolidatedRequirement(
                **candidates[0].model_dump(exclude={"candidate_refs"}), candidate_refs=["CAND-000001"]
            )
            second = ConsolidatedRequirement(
                **candidates[1].model_dump(exclude={"candidate_refs"}), candidate_refs=["CAND-000002"]
            )
            reviews = FakeModel([ReviewResult(
                approved=False,
                duplicate_groups=[DuplicateGroup(
                    requirement_ids=["DREQ-0001", "DREQ-0002"],
                    rationale="Cross-group duplicate.",
                )],
            ), ReviewResult(approved=True)])
            consolidator = FakeModel([
                ConsolidationResult(requirements=[first]),
                ConsolidationResult(requirements=[second]),
                ConsolidationResult(requirements=[ConsolidatedRequirement(
                    name="Merged", category="Functional", statement="The system shall do both.",
                    priority="P2", priority_rationale="Supported.",
                    candidate_refs=["CAND-000001", "CAND-000002"],
                )]),
            ])
            state = self._consolidation_app(
                FakeModel([ExtractionResult(candidates=candidates)]), consolidator, reviews
            ).invoke({
                "input_dir": str(root), "output_dir": str(root / "output"),
                "max_iterations": 1, "consolidation_batch_size": 1,
            })
            self.assertEqual(len(reviews.calls), 2)
            self.assertIn("origin_groups", reviews.calls[0])
            self.assertEqual(len(state["requirements"]), 1)
            self.assertEqual(
                set(state["requirements"][0]["source_documents"]),
                {"a.txt", "b.txt"},
            )

    def test_maximum_one_repair_pass_even_when_second_review_still_flags_issue(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "source.txt").write_text("Supported behavior.", encoding="utf-8")
            candidate = self._consolidation_candidates()[0].model_copy(update={
                "source_documents": ["source.txt"]
            })
            requirement = ConsolidatedRequirement(
                **candidate.model_dump(exclude={"candidate_refs"}), candidate_refs=["CAND-000001"]
            )
            consolidator = FakeModel([
                ConsolidationResult(requirements=[requirement]),
                ConsolidationResult(requirements=[requirement]),
            ])
            reviewer = FakeModel([
                ReviewResult(approved=False, findings=[ReviewFinding(
                    issue="Clarify this requirement.", repair_target="consolidate",
                    affected_requirement_ids=["DREQ-0001"],
                )]),
                ReviewResult(approved=False, findings=[ReviewFinding(
                    issue="Still requires human review.", repair_target="human",
                )]),
            ])
            state = self._consolidation_app(
                FakeModel([ExtractionResult(candidates=[candidate])]), consolidator, reviewer
            ).invoke({
                "input_dir": str(root), "output_dir": str(root / "output"),
                "max_iterations": 1,
            })
            self.assertEqual(len(consolidator.calls), 2)
            self.assertEqual(len(reviewer.calls), 2)
            self.assertEqual(state["iterations"], 1)
            self.assertIn("Still requires human review.", state["findings"][0]["issue"])

    def test_email_source_references_are_recovered_from_candidate_provenance(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "input"
            output = Path(directory) / "output"
            root.mkdir()
            (root / "request.eml").write_text(
                "From: Katherine Gregory <katherine.gregory@gapubliclib.org>\n"
                "Subject: Requirement\n\n"
                "The system shall preserve the requested report.\n",
                encoding="utf-8",
            )
            evidence = "The system shall preserve the requested report."
            candidate = CandidateRequirement(
                name="Preserve report",
                category="Functional",
                statement=evidence,
                priority="P1",
                priority_rationale="Critical operational requirement.",
                priority_is_estimated=False,
                source_documents=["katherine.gregory@gapubliclib.org"],
                evidence=[evidence],
            )
            second_candidate = CandidateRequirement(
                name="Store report",
                category="Functional",
                statement="The system shall store the completed report.",
                priority="P2",
                priority_rationale="Operational need.",
                source_documents=["second.txt"],
                evidence=["The system shall store the completed report."],
            )
            (root / "second.txt").write_text(
                "The system shall store the completed report.",
                encoding="utf-8",
            )
            rejected = RejectedCandidate(
                description="Informal comment",
                source_documents=["katherine.gregory@gapubliclib.org"],
                reason="Not a software requirement.",
            )

            def model_result():
                return ConsolidationResult(requirements=[
                    ConsolidatedRequirement(
                        name="Preserve report",
                        category="Functional",
                        statement=evidence,
                        priority="P1",
                        priority_rationale="Critical operational requirement.",
                        priority_is_estimated=False,
                        source_documents=["katherine.gregory@gapubliclib.org"],
                        evidence=[evidence],
                        candidate_refs=["CAND-000001"],
                    ),
                    ConsolidatedRequirement(
                        name="Store report",
                        category="Functional",
                        statement=second_candidate.statement,
                        priority="P2",
                        priority_rationale="Operational need.",
                        source_documents=["second.txt"],
                        evidence=second_candidate.evidence,
                        candidate_refs=["CAND-000002"],
                    ),
                ])

            def repair_result():
                return ConsolidationResult(requirements=[ConsolidatedRequirement(
                    name="Preserve report",
                    category="Functional",
                    statement=evidence,
                    priority="P1",
                    priority_rationale="Critical operational requirement.",
                    priority_is_estimated=False,
                    source_documents=["katherine.gregory@gapubliclib.org"],
                    evidence=[evidence],
                    candidate_refs=["CAND-000001"],
                )])

            consolidation = FakeModel([model_result(), repair_result()])
            review = FakeModel([
                ReviewResult(approved=False, findings=[ReviewFinding(
                    issue="Clarify the requirement wording.",
                    repair_target="consolidate",
                    affected_requirement_ids=["DREQ-0001"],
                )]),
                ReviewResult(approved=True),
            ])
            state = build_graph(
                FakeModel([ExtractionResult(
                    candidates=[candidate, second_candidate],
                    rejected=[rejected],
                )]),
                consolidation,
                review,
            ).invoke({
                "input_dir": str(root),
                "output_dir": str(output),
                "max_iterations": 1,
            })

            requirements_by_name = {
                item["name"]: item for item in state["requirements"]
            }
            requirement = requirements_by_name["Preserve report"]
            self.assertEqual(requirement["id"], "REQ-001")
            self.assertEqual(requirement["source_documents"], ["request.eml"])
            self.assertEqual(requirement["evidence"], [evidence])
            self.assertEqual(requirement["priority"], "P1")
            self.assertFalse(requirement["manual_review_required"])
            self.assertEqual(state["validation_errors"], [])
            self.assertEqual(state["validation_warnings"], [])
            self.assertEqual(len(consolidation.calls), 2)
            self.assertIn("DREQ-0001", consolidation.calls[-1])
            self.assertEqual(
                requirements_by_name["Store report"]["id"],
                "REQ-002",
            )
            self.assertEqual(
                requirements_by_name["Store report"]["source_documents"],
                ["second.txt"],
            )
            self.assertEqual(state["rejected"][0]["source_documents"], ["request.eml"])

            write_outputs(state, root, output)
            requirements_path = output / "requirements.md"
            summary_path = output / "run_summary.json"
            self.assertTrue(requirements_path.is_file())
            self.assertTrue(summary_path.is_file())
            requirements_text = requirements_path.read_text(encoding="utf-8")
            self.assertIn("request.eml", requirements_text)
            self.assertIn(evidence, requirements_text)
            self.assertIn("Blacklist of rejected candidates", requirements_text)
            self.assertNotIn("katherine.gregory@gapubliclib.org", requirements_text)
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
            self.assertEqual(summary["requirement_count"], 2)
            self.assertEqual(summary["rejected_candidate_count"], 1)
            self.assertEqual(summary["validation_warnings"], [])

            cached_consolidator = FakeModel([])
            cached_state = build_graph(
                FakeModel([]),
                cached_consolidator,
                FakeModel([
                    ReviewResult(approved=False, findings=[ReviewFinding(
                        issue="Clarify the requirement wording.",
                        repair_target="consolidate",
                        affected_requirement_ids=["DREQ-0001"],
                    )]),
                    ReviewResult(approved=True),
                ]),
            ).invoke({
                "input_dir": str(root),
                "output_dir": str(output),
                "max_iterations": 1,
            })
            self.assertEqual(cached_consolidator.calls, [])
            self.assertEqual(
                next(
                    item for item in cached_state["requirements"]
                    if item["name"] == "Preserve report"
                )["source_documents"],
                ["request.eml"],
            )

    def test_consolidation_timeout_resumes_cached_group(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "input"
            output = Path(directory) / "output"
            root.mkdir()
            for index in range(1, 5):
                (root / f"source-{index}.txt").write_text(f"Source {index}", encoding="utf-8")
            candidates = self._consolidation_candidates()
            first_group = ConsolidationResult(requirements=[
                ConsolidatedRequirement(
                    **candidates[0].model_dump(exclude={"candidate_refs"}),
                    candidate_refs=["CAND-000001", "CAND-000002"],
                ),
            ])
            second_group = ConsolidationResult(requirements=[
                ConsolidatedRequirement(
                    **candidates[2].model_dump(exclude={"candidate_refs"}),
                    candidate_refs=["CAND-000003", "CAND-000004"],
                ),
            ])
            failed_consolidator = FakeModel([
                first_group,
                TimeoutError("request timed out"),
            ])
            first_app = self._consolidation_app(
                FakeModel([ExtractionResult(candidates=candidates)]),
                failed_consolidator,
                FakeModel([]),
            )
            with self.assertLogs("requirements_agent", level="ERROR") as captured:
                with self.assertRaises(TimeoutError):
                    first_app.invoke({
                        "input_dir": str(root),
                        "output_dir": str(output),
                        "max_iterations": 0,
                        "consolidation_batch_size": 2,
                    })
            failure_log = "\n".join(captured.output)
            self.assertIn("skupina 2/2", failure_log)
            self.assertIn("consolidate-model", failure_log)
            self.assertIn("request timed out", failure_log)
            self.assertFalse((output / "requirements.md").exists())
            self.assertTrue((output / ".cache" / "consolidation_cache.json").exists())

            resumed_consolidator = FakeModel([second_group])
            resumed_app = self._consolidation_app(
                FakeModel([ExtractionResult(candidates=candidates)]),
                resumed_consolidator,
                FakeModel([ReviewResult(approved=True)]),
            )
            with self.assertLogs("requirements_agent", level="INFO") as captured:
                state = resumed_app.invoke({
                    "input_dir": str(root),
                    "output_dir": str(output),
                    "max_iterations": 0,
                    "consolidation_batch_size": 2,
                })
            resume_log = "\n".join(captured.output)
            self.assertIn("Načítavam konsolidáciu skupiny 1/2 z cache", resume_log)
            self.assertEqual(len(resumed_consolidator.calls), 1)
            self.assertEqual(len(state["requirements"]), 2)
            self.assertEqual(
                state["requirements"][1]["source_documents"],
                ["source-3.txt", "source-4.txt"],
            )

    def test_extraction_cache_requires_matching_input_model_and_prompt_version(self):
        with tempfile.TemporaryDirectory() as directory:
            cache = ExtractionCache(Path(directory))
            documents = [{"id": "source.txt", "name": "source.txt", "text": "Example"}]
            result = ExtractionResult()
            cache.put("extract-model", "prompt-v1", documents, result)
            self.assertIsNotNone(cache.get("extract-model", "prompt-v1", documents))
            cache.put("extract-model", "prompt-v1", documents, result, "review feedback")
            self.assertIsNone(
                cache.get("extract-model", "prompt-v1", documents, "other feedback")
            )
            self.assertIsNotNone(
                cache.get("extract-model", "prompt-v1", documents, "review feedback")
            )
            self.assertIsNone(cache.get("different-model", "prompt-v1", documents))
            self.assertIsNone(cache.get("extract-model", "prompt-v2", documents))
            changed_documents = [{**documents[0], "text": "Changed"}]
            self.assertIsNone(cache.get("extract-model", "prompt-v1", changed_documents))
            cache_text = cache.path.read_text(encoding="utf-8")
            self.assertNotIn("OPENAI_API_KEY", cache_text)

    def test_failed_extraction_resumes_from_successful_cached_batches(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "input"
            output = Path(directory) / "output"
            root.mkdir()
            (root / "one.txt").write_text("12345", encoding="utf-8")
            (root / "two.txt").write_text("abcde", encoding="utf-8")
            first_candidate = CandidateRequirement(
                name="First requirement",
                category="Functional",
                statement="The system shall perform the first action.",
                priority="P3",
                priority_rationale="Estimated.",
                source_documents=["one.txt"],
            )
            second_candidate = CandidateRequirement(
                name="Second requirement",
                category="Functional",
                statement="The system shall perform the second action.",
                priority="P3",
                priority_rationale="Estimated.",
                source_documents=["two.txt"],
            )
            names = {
                "extraction": "extract-model",
                "consolidation": "consolidate-model",
                "review": "review-model",
            }
            first_extractor = FakeModel([
                ExtractionResult(candidates=[first_candidate]),
                TimeoutError("request timed out"),
            ])
            first_app = build_graph(
                first_extractor,
                FakeModel([]),
                FakeModel([]),
                model_names=names,
                extraction_batch_chars=5,
            )
            with self.assertLogs("requirements_agent", level="INFO") as captured:
                with self.assertRaises(TimeoutError):
                    first_app.invoke({
                        "input_dir": str(root),
                        "output_dir": str(output),
                        "max_iterations": 0,
                    })
            first_logs = "\n".join(captured.output)
            self.assertIn("dávka 2/2 definitívne zlyhala", first_logs)
            self.assertTrue((output / ".cache" / "extraction_cache.json").exists())
            self.assertFalse((output / "requirements.md").exists())
            self.assertEqual(len(first_extractor.calls), 2)

            resumed_extractor = FakeModel([ExtractionResult(candidates=[second_candidate])])
            consolidated = ConsolidatedRequirement(
                name="Combined requirements",
                category="Functional",
                statement="The system shall perform both supported actions.",
                priority="P3",
                priority_rationale="Estimated.",
                source_documents=["one.txt", "two.txt"],
                candidate_refs=["CAND-000001", "CAND-000002"],
            )
            resumed_app = build_graph(
                resumed_extractor,
                FakeModel([ConsolidationResult(requirements=[consolidated])]),
                FakeModel([ReviewResult(approved=True), ReviewResult(approved=True)]),
                model_names=names,
                extraction_batch_chars=5,
            )
            with self.assertLogs("requirements_agent", level="INFO") as captured:
                state = resumed_app.invoke({
                    "input_dir": str(root),
                    "output_dir": str(output),
                    "max_iterations": 0,
                })
            resumed_logs = "\n".join(captured.output)
            self.assertIn("Používam uložený výsledok extrakcie pre dávku 1/2", resumed_logs)
            self.assertEqual(len(resumed_extractor.calls), 1)
            self.assertEqual(state["requirements"][0]["source_documents"], ["one.txt", "two.txt"])

    def test_review_feedback_loops_to_consolidation_and_ids_are_assigned(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "input"
            root.mkdir()
            (root / "source.txt").write_text("System must produce a report.", encoding="utf-8")
            source = "source.txt"
            candidate = CandidateRequirement(
                name="Produce reports",
                category="Functional",
                statement="The system shall produce reports.",
                priority="P2",
                priority_rationale="Explicit operational need.",
                priority_is_estimated=False,
                source_documents=[source],
                evidence=["System must produce a report."],
            )
            extraction = FakeModel([ExtractionResult(candidates=[candidate])])
            consolidated = ConsolidatedRequirement(
                **candidate.model_dump(exclude={"candidate_refs"}),
                candidate_refs=["CAND-000001"],
            )
            consolidation = FakeModel([
                ConsolidationResult(requirements=[consolidated]),
                ConsolidationResult(requirements=[consolidated]),
            ])
            review = FakeModel([
                ReviewResult(
                    approved=False,
                    findings=[ReviewFinding(
                        issue="Clarify report scope.",
                        repair_target="consolidate",
                        evidence=["The source does not specify report scope."],
                        affected_requirement_ids=["DREQ-0001"],
                    )],
                ),
                ReviewResult(approved=True),
            ])
            app = build_graph(extraction, consolidation, review)
            state = app.invoke({
                "input_dir": str(root),
                "output_dir": str(root / "output"),
                "max_iterations": 1,
            })
            self.assertEqual(len(consolidation.calls), 2)
            self.assertEqual(state["iterations"], 1)
            self.assertEqual(state["requirements"][0]["id"], "REQ-001")
            self.assertEqual(state["requirements"][0]["source_documents"], [source])
            self.assertEqual(state["validation_errors"], [])

    def test_feedback_stops_at_iteration_limit(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "source.txt").write_text("A supported requirement.", encoding="utf-8")
            candidate = CandidateRequirement(
                name="Requirement",
                category="Functional",
                statement="The system shall do the supported action.",
                priority="P3",
                priority_rationale="Estimated.",
                source_documents=["source.txt"],
            )
            extraction = FakeModel([ExtractionResult(candidates=[candidate])])
            consolidation = FakeModel([
                ConsolidationResult(requirements=[ConsolidatedRequirement(
                    **candidate.model_dump(exclude={"candidate_refs"}),
                    candidate_refs=["CAND-000001"],
                )]),
                ConsolidationResult(requirements=[ConsolidatedRequirement(
                    **candidate.model_dump(exclude={"candidate_refs"}),
                    candidate_refs=["CAND-000001"],
                )]),
            ])
            review = FakeModel([
                ReviewResult(approved=False, findings=[
                    ReviewFinding(
                        issue="Fix wording.",
                        repair_target="consolidate",
                        affected_requirement_ids=["DREQ-0001"],
                    )
                ]),
                ReviewResult(approved=False, findings=[
                    ReviewFinding(issue="Still needs a human.", repair_target="human")
                ]),
            ])
            state = build_graph(extraction, consolidation, review).invoke({
                "input_dir": str(root),
                "output_dir": str(root / "output"),
                "max_iterations": 1,
            })
            self.assertEqual(len(review.calls), 2)
            self.assertEqual(state["iterations"], 1)
            self.assertEqual(state["requirements"][0]["id"], "REQ-001")

    def test_graph_logs_progress_without_document_text(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "source.txt").write_text(
                "PRIVATE_DOCUMENT_TEXT should never appear in logs.",
                encoding="utf-8",
            )
            candidate = CandidateRequirement(
                name="Requirement",
                category="Functional",
                statement="The system shall do the supported action.",
                priority="P3",
                priority_rationale="Estimated.",
                source_documents=["source.txt"],
            )
            app = build_graph(
                FakeModel([ExtractionResult(candidates=[candidate])]),
                FakeModel([ConsolidationResult(
                    requirements=[ConsolidatedRequirement(
                        **candidate.model_dump(exclude={"candidate_refs"}),
                        candidate_refs=["CAND-000001"],
                    )]
                )]),
                FakeModel([ReviewResult(approved=True)]),
                model_names={
                    "extraction": "extract-test",
                    "consolidation": "consolidate-test",
                    "review": "review-test",
                },
                api_secret="sk-test-secret-123456789",
            )
            with self.assertLogs("requirements_agent", level="INFO") as captured:
                app.invoke({
                    "input_dir": str(root),
                    "output_dir": str(root / "output"),
                    "max_iterations": 0,
                })
            output = "\n".join(captured.output)
            self.assertIn("Načítaných 1 dokumentov", output)
            self.assertIn("uzol extrakcia, model extract-test", output)
            self.assertIn("uzol konsolidácia skupina 1/1, model consolidate-test", output)
            self.assertIn("uzol globálna kontrola, model review-test", output)
            self.assertNotIn("PRIVATE_DOCUMENT_TEXT", output)
            self.assertNotIn("sk-test-secret-123456789", output)

    def test_unrecoverable_source_is_a_manual_review_warning(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "source.txt").write_text("A supported requirement.", encoding="utf-8")
            candidate = CandidateRequirement(
                name="Requirement",
                category="Functional",
                statement="The system shall do the supported action.",
                priority="P3",
                priority_rationale="Estimated.",
                source_documents=["unknown.txt"],
            )
            app = build_graph(
                FakeModel([ExtractionResult(candidates=[candidate])]),
                FakeModel([ConsolidationResult(
                    requirements=[ConsolidatedRequirement(
                        **candidate.model_dump(exclude={"candidate_refs"}),
                        candidate_refs=["CAND-000001"],
                    )]
                )]),
                FakeModel([ReviewResult(approved=True)]),
            )
            state = app.invoke({
                "input_dir": str(root),
                "output_dir": str(root / "output"),
                "max_iterations": 0,
            })
            self.assertEqual(state["validation_errors"], [])
            self.assertTrue(state["requirements"][0]["manual_review_required"])
            self.assertEqual(state["requirements"][0]["source_documents"], [])
            self.assertTrue(any("could not be reliably mapped" in warning for warning in state["validation_warnings"]))
            write_outputs(state, root, root / "output")
            self.assertTrue((root / "output" / "requirements.md").exists())
            self.assertTrue((root / "output" / "run_summary.json").exists())
            self.assertEqual(state["requirements"][0]["id"], "REQ-001")

    def test_unknown_sources_remain_invalid_in_deterministic_validation(self):
        self.assertEqual(
            _unknown_sources(
                ["katherine.gregory@gapubliclib.org", "missing.txt", "source.txt"],
                {"source.txt"},
            ),
            ["katherine.gregory@gapubliclib.org", "missing.txt"],
        )


class ProgressTests(unittest.TestCase):
    def test_long_call_logs_wait_warning_and_completes(self):
        class SlowModel:
            def invoke(self, _prompt):
                del _prompt
                time.sleep(0.05)
                return "done"

        with self.assertLogs("requirements_agent", level="INFO") as captured:
            result = timed_invoke(
                SlowModel(),
                "private prompt text",
                node="test",
                model_name="offline-model",
                warning_after=0.01,
            )
        self.assertEqual(result, "done")
        self.assertTrue(any("Stále čakám na odpoveď API" in line for line in captured.output))
        self.assertTrue(any("API odpovedalo" in line for line in captured.output))
        self.assertFalse(any("private prompt text" in line for line in captured.output))

    def test_failed_call_logs_error_without_api_secret(self):
        class BrokenModel:
            def invoke(self, _prompt):
                del _prompt
                raise RuntimeError("Authorization: Bearer secret-token sk-test-secret-123456789")

        with self.assertLogs("requirements_agent", level="ERROR") as captured:
            with self.assertRaises(RuntimeError):
                timed_invoke(
                    BrokenModel(),
                    "private prompt text",
                    node="test",
                    model_name="offline-model",
                    secret="sk-test-secret-123456789",
                )
        output = "\n".join(captured.output)
        self.assertIn("RuntimeError", output)
        self.assertNotIn("secret-token", output)
        self.assertNotIn("sk-test-secret-123456789", output)
        self.assertNotIn("private prompt text", output)


if __name__ == "__main__":
    unittest.main()
