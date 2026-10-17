"""Calculate per-question multiset Jaccard similarity for Task 2 predictions."""

import csv
import html
import importlib.util
import json
import sqlite3
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean, median

TASK_DIR = Path(__file__).resolve().parent
DATA_DIR = TASK_DIR.parent / "Task_2" / "data"
EVALUATOR_PATH = DATA_DIR / "evaluate_retrieval_predictions.py"
LABELS_PATH = DATA_DIR / "restaurants_dataset.csv"
TASK2_METRICS_PATH = DATA_DIR / "task2_metrics.json"
OUTPUT_METRICS_PATH = TASK_DIR / "task3_metrics.json"
OUTPUT_SCORES_PATH = TASK_DIR / "task3_per_question_scores.csv"
OUTPUT_REPORT_PATH = TASK_DIR / "task3_report.md"
EXPECTED_QUESTIONS = 155
FRAMEWORKS = ("RTF", "ICIO", "CRISP")
PREDICTION_FIELDS = {"question", "predicted_sql", "framework", "generation_status"}
SCORE_FIELDS = (
    "question_index",
    "question",
    "framework",
    "generation_status",
    "predicted_row_count",
    "reference_row_count",
    "intersection_count",
    "union_count",
    "multiset_jaccard_similarity",
    "exact_match",
    "error_type",
    "error",
)

_evaluator_spec = importlib.util.spec_from_file_location(
    "task2_reference_evaluator", EVALUATOR_PATH
)
if _evaluator_spec is None or _evaluator_spec.loader is None:
    raise ImportError(f"Could not load the original evaluator at {EVALUATOR_PATH}")
_evaluator_module = importlib.util.module_from_spec(_evaluator_spec)
_evaluator_spec.loader.exec_module(_evaluator_module)
load_database = _evaluator_module.load_database


def read_labels():
    csv.field_size_limit(1_000_000_000)
    labels = []
    with LABELS_PATH.open(encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        if reader.fieldnames is None or not {"question", "result"}.issubset(
            reader.fieldnames
        ):
            raise ValueError(f"Unexpected dataset columns in {LABELS_PATH}")
        for line_number, row in enumerate(reader, start=2):
            try:
                result = json.loads(row["result"])
            except json.JSONDecodeError as error:
                raise ValueError(
                    f"Invalid JSON reference result on line {line_number}"
                ) from error
            if not isinstance(result, list):
                raise ValueError(
                    f"Expected a JSON array reference result on line {line_number}"
                )
            if not all(isinstance(result_row, list) for result_row in result):
                raise ValueError(
                    f"Expected reference rows to be JSON arrays on line {line_number}"
                )
            labels.append((row["question"], result))
    if len(labels) != EXPECTED_QUESTIONS:
        raise ValueError(
            f"Expected {EXPECTED_QUESTIONS} reference questions, found {len(labels)}"
        )
    return labels


def read_predictions(framework, labels):
    path = DATA_DIR / f"task2_predictions_{framework.lower()}.csv"
    if not path.is_file():
        raise FileNotFoundError(f"Missing prediction CSV: {path}")

    with path.open(encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        if reader.fieldnames is None or not PREDICTION_FIELDS.issubset(
            reader.fieldnames
        ):
            raise ValueError(f"Missing required prediction columns in {path}")
        rows = list(reader)

    if len(rows) != EXPECTED_QUESTIONS:
        raise ValueError(
            f"{framework} contains {len(rows)} prediction rows; "
            f"expected {EXPECTED_QUESTIONS}"
        )
    expected_questions = [question for question, _ in labels]
    if [row["question"] for row in rows] != expected_questions:
        raise ValueError(
            f"{framework} question text or ordering does not match the dataset"
        )
    if any(row["framework"] != framework for row in rows):
        raise ValueError(f"{framework} CSV contains a mismatched framework label")
    return rows


def multiset_jaccard(predicted_rows, reference_rows):
    """Return similarity and multiset intersection/union sizes."""
    predicted = Counter(tuple(row) for row in predicted_rows)
    reference = Counter(tuple(row) for row in reference_rows)
    intersection = sum((predicted & reference).values())
    union = sum((predicted | reference).values())
    score = intersection / union if union else 1.0
    return score, intersection, union


def allow_read_only_sql(action, _arg1, _arg2, _database, _trigger):
    _ = (_arg1, _arg2, _database, _trigger)
    allowed_actions = {
        sqlite3.SQLITE_SELECT,
        sqlite3.SQLITE_READ,
        sqlite3.SQLITE_FUNCTION,
    }
    if hasattr(sqlite3, "SQLITE_RECURSIVE"):
        allowed_actions.add(sqlite3.SQLITE_RECURSIVE)
    return (
        sqlite3.SQLITE_OK
        if action in allowed_actions
        else sqlite3.SQLITE_DENY
    )


def score_framework(framework, labels, predictions, connection):
    scores = []
    for index, ((question, reference_rows), prediction) in enumerate(
        zip(labels, predictions), start=1
    ):
        status = prediction["generation_status"]
        error_type = ""
        error = ""
        predicted_rows = []
        intersection = 0
        union = 0

        if status != "SUCCESS":
            error_type = "generation_failure"
            error = prediction.get("error", "") or (
                f"Generation status was {status or 'empty'}."
            )
            score = 0.0
        else:
            try:
                cursor = connection.execute(prediction["predicted_sql"])
                predicted_rows = cursor.fetchall()
                score, intersection, union = multiset_jaccard(
                    predicted_rows, reference_rows
                )
            except sqlite3.Error as error_value:
                error_type = "sql_execution_error"
                error = str(error_value)
                score = 0.0

        scores.append(
            {
                "question_index": index,
                "question": question,
                "framework": framework,
                "generation_status": status,
                "predicted_row_count": len(predicted_rows),
                "reference_row_count": len(reference_rows),
                "intersection_count": intersection,
                "union_count": union,
                "multiset_jaccard_similarity": score,
                "exact_match": score == 1.0,
                "error_type": error_type,
                "error": error,
            }
        )
    return scores


def summarize_framework(framework, scores, expected_task2_metrics):
    values = [item["multiset_jaccard_similarity"] for item in scores]
    exact_count = sum(value == 1.0 for value in values)
    partial_count = sum(0.0 < value < 1.0 for value in values)
    zero_count = sum(value == 0.0 for value in values)
    execution_errors = sum(
        item["error_type"] == "sql_execution_error" for item in scores
    )
    failed_predictions = sum(
        item["error_type"] == "generation_failure" for item in scores
    )
    task2_expected = expected_task2_metrics.get(framework)
    if task2_expected is None:
        raise ValueError(f"Missing Task 2 metrics for {framework}")
    if task2_expected.get("correct") != exact_count:
        raise ValueError(
            f"{framework}: Task 3 exact-match count {exact_count} does not agree "
            f"with Task 2 evaluator count {task2_expected.get('correct')}"
        )
    if task2_expected.get("total_questions") != len(scores):
        raise ValueError(
            f"{framework}: Task 2 denominator does not match Task 3 score count"
        )

    return {
        "framework": framework,
        "total_questions": len(scores),
        "mean_multiset_jaccard_similarity": mean(values),
        "median_multiset_jaccard_similarity": median(values),
        "perfect_similarity_count": exact_count,
        "partial_similarity_count": partial_count,
        "zero_similarity_count": zero_count,
        "sql_execution_errors": execution_errors,
        "failed_predictions": failed_predictions,
        "accuracy_correct": exact_count,
        "accuracy": exact_count / len(scores),
        "accuracy_source": "Task 2 authoritative evaluator; independently cross-checked",
    }


def write_scores_csv(scores_by_framework):
    with OUTPUT_SCORES_PATH.open("w", encoding="utf-8", newline="") as destination:
        writer = csv.DictWriter(destination, fieldnames=SCORE_FIELDS)
        writer.writeheader()
        for framework in FRAMEWORKS:
            for row in scores_by_framework[framework]:
                writer.writerow(row)


def svg_mean_similarity(summaries):
    width, height = 760, 390
    left, top, plot_width, plot_height = 80, 45, 620, 250
    colors = {"RTF": "#3b82f6", "ICIO": "#10b981", "CRISP": "#f59e0b"}
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<text x="380" y="25" text-anchor="middle" font-family="Arial" font-size="18" font-weight="bold">Mean Multiset Jaccard Similarity</text>',
    ]
    for tick in range(0, 101, 20):
        y = top + plot_height * (100 - tick) / 100
        parts.extend(
            [
                f'<line x1="{left}" y1="{y:.1f}" x2="{left + plot_width}" y2="{y:.1f}" stroke="#d9e0e8"/>',
                f'<text x="{left - 12}" y="{y + 4:.1f}" text-anchor="end" font-family="Arial" font-size="12" fill="#445">{tick}%</text>',
            ]
        )
    bar_width, gap, start_x = 110, 80, left + 50
    for index, item in enumerate(summaries):
        value = item["mean_multiset_jaccard_similarity"]
        x = start_x + index * (bar_width + gap)
        bar_height = plot_height * value
        y = top + plot_height - bar_height
        parts.extend(
            [
                f'<rect x="{x}" y="{y:.1f}" width="{bar_width}" height="{bar_height:.1f}" rx="5" fill="{colors[item["framework"]]}"/>',
                f'<text x="{x + bar_width / 2}" y="{max(top + 15, y - 8):.1f}" text-anchor="middle" font-family="Arial" font-size="14" font-weight="bold">{value:.6f}</text>',
                f'<text x="{x + bar_width / 2}" y="{top + plot_height + 23}" text-anchor="middle" font-family="Arial" font-size="14">{html.escape(item["framework"])}</text>',
                f'<text x="{x + bar_width / 2}" y="{top + plot_height + 43}" text-anchor="middle" font-family="Arial" font-size="11" fill="#445">{item["perfect_similarity_count"]}/{item["total_questions"]} exact</text>',
            ]
        )
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def write_report(summaries, model_metadata, scores_by_framework):
    table_rows = []
    for item in summaries:
        table_rows.append(
            "| {framework} | {accuracy_correct}/{total_questions} "
            "| {accuracy:.2%} | {mean_multiset_jaccard_similarity:.6f} "
            "| {median_multiset_jaccard_similarity:.6f} "
            "| {perfect_similarity_count} | {partial_similarity_count} "
            "| {zero_similarity_count} | {sql_execution_errors} "
            "| {failed_predictions} |".format(**item)
        )

    model_setting = model_metadata.get("model_setting", "not recorded")
    actual_model_ids = sorted(
        {
            model_id
            for session in model_metadata.get("sessions", {}).values()
            for model_id in session.get("actual_model_ids", [])
        }
    )
    model_ids_text = ", ".join(f"`{value}`" for value in actual_model_ids) or "not recorded"
    partial_counts = {
        item["partial_similarity_count"] for item in summaries
    }
    if len(partial_counts) == 1:
        partial_count = partial_counts.pop()
        if partial_count == 0:
            partial_result_note = (
                "There were no partially overlapping result sets: every score "
                "was either exactly 1 or 0."
            )
        else:
            partial_scores = [
                f"{framework} Q{score['question_index']}="
                f"{score['multiset_jaccard_similarity']:.6f}"
                for framework in FRAMEWORKS
                for score in scores_by_framework[framework]
                if 0.0 < score["multiset_jaccard_similarity"] < 1.0
            ]
            partial_result_note = (
                f"Each framework had {partial_count} partially overlapping "
                "result set(s) (" + ", ".join(partial_scores) + ")."
            )
    else:
        partial_result_note = (
            "Partial-overlap counts differ among frameworks; see the table."
        )

    report = f"""# Task 3: Multiset Jaccard Similarity for Text-to-SQL

## Introduction and motivation

Task 2 evaluated each generated SQL query with exact result-set accuracy: a prediction is correct only when its complete result multiset matches the reference. This is useful for strict correctness, but it gives the same zero credit to a query with nearly all expected rows and one with no matching rows. This report adds a graded measure of result overlap while retaining exact accuracy as the primary all-or-nothing measure.

The Task 2 benchmark contains {summaries[0]['total_questions']} questions per framework. The configured model setting was `{model_setting}`; recorded response model IDs were {model_ids_text}. No benchmark sessions were run and no predictions were regenerated for Task 3.

## Metric definition

For each question, let *A* be the multiset of rows returned by the predicted SQL query and *B* be the reference-result multiset. A multiset records each row together with its occurrence count. The Multiset Jaccard Similarity is:

`J(A, B) = sum_r min(c_A(r), c_B(r)) / sum_r max(c_A(r), c_B(r))`

where `c_A(r)` and `c_B(r)` are the multiplicities of row `r` in the predicted and reference results. The numerator is the multiset intersection size; the denominator is the multiset union size. Counting multiplicities means duplicate rows are preserved, consistently with the Task 2 evaluator.

If both result multisets are empty, the union size is zero and the score is defined as 1. If exactly one is empty, the score is 0. Identical multisets, including duplicates, score 1; disjoint multisets score 0; partial overlap scores strictly between 0 and 1. A failed generation or SQL execution error receives score 0 and is separately counted, so it cannot disappear from the fixed denominator of {summaries[0]['total_questions']}.

## Why the metric is appropriate

Text-to-SQL result errors can be incremental: a query may return many of the right rows while missing some rows or including a few extras. Exact accuracy does not distinguish such a result from a wholly unrelated one. Multiset Jaccard gives partial credit for overlap and penalizes both omissions and excess rows. It is interpretable on a 0–1 scale and uses the same executed predictions, database, reference results, row equality, and duplicate-sensitive semantics as the existing evaluator.

This metric **complements and does not replace** exact result accuracy. A score below 1 is not a correct answer under the original benchmark. Exact accuracy remains necessary for strict correctness; the average Jaccard score describes the degree of row overlap among all questions.

## Implementation

`calculate_task3_metric.py` loads the original 155 question/reference pairs and each existing Task 2 prediction CSV, verifies row counts, question order, and framework labels, then builds the SQLite database using the unchanged `load_database` implementation from `evaluate_retrieval_predictions.py`. SQL executes in the in-memory database with SQLite authorization restricted to read-only `SELECT`/`READ`/function operations; multi-statement SQL is rejected by SQLite's single-statement `execute` API. The script continues after a generation or SQL execution failure, records its type and message, assigns score 0, and includes that question in every aggregate's denominator.

The per-question results are in [`task3_per_question_scores.csv`](task3_per_question_scores.csv), and the summary is in [`task3_metrics.json`](task3_metrics.json). Task 2's authoritative `Correct` count is cross-checked against the number of Task 3 scores equal to 1.

## Results

| Framework | Exact correct | Exact accuracy | Mean Jaccard | Median Jaccard | Score 1 | Partial (0 < J < 1) | Score 0 | SQL errors | Failed predictions |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
{chr(10).join(table_rows)}

![Mean Multiset Jaccard Similarity by framework](task3_mean_similarity.svg)

## Interpretation

All three frameworks' exact-match counts are verified against the Task 2 evaluator. In this run the frameworks tie: each has mean Jaccard {summaries[0]['mean_multiset_jaccard_similarity']:.6f}, median {summaries[0]['median_multiset_jaccard_similarity']:.6f}, and the same counts in every score category. The mean is only slightly above exact accuracy because the one partial result per framework has a very small overlap; the median remains zero because more than half of the questions have score zero. This shows why the graded measure complements, rather than overturns, the exact-match result. A framework could rank differently on graded overlap in another dataset, but no such difference appears here.

The aggregate values above are calculated over all {summaries[0]['total_questions']} questions for each framework. {partial_result_note} SQL errors and failed generations, if any, are visible in separate columns and have zero similarity rather than being omitted.

## Limitations

- Row overlap is not a complete measure of semantic correctness. Missing or extra rows may have different importance, while Jaccard treats each row occurrence equally.
- A partly overlapping result can still be misleading for the user's intent; conversely, queries with different SQL text can be semantically equivalent when their result multisets match.
- Jaccard compares returned row values, not query structure, execution efficiency, or whether a query generalizes beyond this fixed database.
- The benchmark contains one prediction per question and framework. This report is descriptive and makes no claim of statistical significance.

"""
    OUTPUT_REPORT_PATH.write_text(report, encoding="utf-8")


def main():
    labels = read_labels()
    task2_data = json.loads(TASK2_METRICS_PATH.read_text(encoding="utf-8"))
    task2_metrics = {
        item["framework"]: item for item in task2_data.get("metrics", [])
    }

    connection = load_database()
    connection.set_authorizer(allow_read_only_sql)
    try:
        scores_by_framework = {}
        summaries = []
        for framework in FRAMEWORKS:
            predictions = read_predictions(framework, labels)
            scores = score_framework(framework, labels, predictions, connection)
            scores_by_framework[framework] = scores
            summaries.append(
                summarize_framework(framework, scores, task2_metrics)
            )
    finally:
        connection.close()

    write_scores_csv(scores_by_framework)
    (TASK_DIR / "task3_mean_similarity.svg").write_text(
        svg_mean_similarity(summaries), encoding="utf-8"
    )
    write_report(
        summaries,
        json.loads(
            (DATA_DIR / "task2_experiment_metadata.json").read_text(
                encoding="utf-8"
            )
        ),
        scores_by_framework,
    )
    metrics_output = {
        "metric": "Multiset Jaccard Similarity",
        "metric_definition": (
            "sum_r min(c_A(r), c_B(r)) / sum_r max(c_A(r), c_B(r)); "
            "defined as 1 when both multisets are empty"
        ),
        "complements_exact_accuracy": True,
        "denominator_per_framework": EXPECTED_QUESTIONS,
        "source_data": {
            "labels": str(LABELS_PATH.relative_to(TASK_DIR.parent)),
            "predictions": [
                str(
                    (DATA_DIR / f"task2_predictions_{framework.lower()}.csv")
                    .relative_to(TASK_DIR.parent)
                )
                for framework in FRAMEWORKS
            ],
            "database_loader": "evaluate_retrieval_predictions.py:load_database",
            "task2_accuracy_cross_check": str(
                TASK2_METRICS_PATH.relative_to(TASK_DIR.parent)
            ),
        },
        "evaluated_utc": datetime.now(timezone.utc).isoformat(),
        "summaries": summaries,
    }
    OUTPUT_METRICS_PATH.write_text(
        json.dumps(metrics_output, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print("Framework | Exact | Mean Jaccard | Median | Partial | Zero | SQL errors | Failed")
    for item in summaries:
        print(
            f"{item['framework']} | {item['accuracy_correct']}/"
            f"{item['total_questions']} | "
            f"{item['mean_multiset_jaccard_similarity']:.4f} | "
            f"{item['median_multiset_jaccard_similarity']:.4f} | "
            f"{item['partial_similarity_count']} | "
            f"{item['zero_similarity_count']} | "
            f"{item['sql_execution_errors']} | {item['failed_predictions']}"
        )
    print("Task 3 scores, metrics, chart, and report written.")


if __name__ == "__main__":
    main()
