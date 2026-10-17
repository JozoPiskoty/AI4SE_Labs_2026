"""Evaluate Task 2 prediction CSVs and generate a metrics report with SVG charts."""

import csv
import hashlib
import html
import json
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean, median


TASK_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = TASK_DIR / "data"
LABELS_PATH = DATA_DIR / "restaurants_dataset.csv"
SCHEMA_PATH = DATA_DIR / "restaurants-schema.csv"
DATABASE_PATH = DATA_DIR / "restaurants-db.txt"
TEACHER_EVALUATOR_PATH = DATA_DIR / "evaluate_retrieval_predictions.py"
METADATA_PATH = DATA_DIR / "task2_experiment_metadata.json"
METRICS_PATH = DATA_DIR / "task2_metrics.json"
REPORT_PATH = TASK_DIR / "task2_report.md"
EXPECTED_QUESTIONS = 155
FRAMEWORKS = ("RTF", "ICIO", "CRISP")
PREDICTION_FIELDS = {
    "question",
    "predicted_sql",
    "framework",
    "model_id",
    "generation_time_seconds",
    "generation_status",
    "error",
    "attempt_count",
    "session_id",
    "request_id",
}
def read_labels():
    csv.field_size_limit(1_000_000_000)
    labels = []
    with LABELS_PATH.open(encoding="utf-8-sig", newline="") as source:
        for line_number, row in enumerate(csv.DictReader(source), start=2):
            try:
                result = json.loads(row["result"])
            except json.JSONDecodeError as error:
                raise ValueError(
                    f"Invalid JSON label result on line {line_number}"
                ) from error
            if not isinstance(result, list):
                raise ValueError(
                    f"Expected a JSON array label result on line {line_number}"
                )
            labels.append((row["question"], result))
    if len(labels) != EXPECTED_QUESTIONS:
        raise ValueError(
            f"Expected {EXPECTED_QUESTIONS} reference rows, found {len(labels)}"
        )
    return labels


def read_predictions(framework, labels):
    path = DATA_DIR / f"task2_predictions_{framework.lower()}.csv"
    if not path.is_file():
        raise FileNotFoundError(f"Missing prediction file: {path}")
    with path.open(encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        if reader.fieldnames is None or not PREDICTION_FIELDS.issubset(
            reader.fieldnames
        ):
            raise ValueError(f"Missing required prediction columns in {path}")
        rows = list(reader)
    if len(rows) != EXPECTED_QUESTIONS:
        raise ValueError(
            f"{framework} has {len(rows)} rows; expected {EXPECTED_QUESTIONS}"
        )
    if [row["question"] for row in rows] != [question for question, _ in labels]:
        raise ValueError(
            f"{framework} question text/order does not exactly match the labels."
        )
    if any(row["framework"] != framework for row in rows):
        raise ValueError(f"{framework} CSV contains a mismatched framework value.")
    return rows


def run_teacher_evaluator(framework):
    if not TEACHER_EVALUATOR_PATH.is_file():
        raise FileNotFoundError(f"Missing original evaluator: {TEACHER_EVALUATOR_PATH}")

    with tempfile.TemporaryDirectory(
        prefix=f"task2-evaluator-{framework.lower()}-"
    ) as temporary_directory:
        work_dir = Path(temporary_directory)
        for source in (
            TEACHER_EVALUATOR_PATH,
            LABELS_PATH,
            SCHEMA_PATH,
            DATABASE_PATH,
        ):
            shutil.copy2(source, work_dir / source.name)

        prediction_source = DATA_DIR / f"task2_predictions_{framework.lower()}.csv"
        shutil.copy2(
            prediction_source,
            work_dir / "restaurants_dataset_predictions.csv",
        )

        completed = subprocess.run(
            [sys.executable, TEACHER_EVALUATOR_PATH.name],
            cwd=work_dir,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if completed.returncode != 0:
            evaluator_output = f"{completed.stdout}\n{completed.stderr}".strip()
            sql_error_match = re.search(
                r"Could not execute predicted SQL on line (\d+)", evaluator_output
            )
            if sql_error_match:
                raise RuntimeError(
                    f"The original evaluator encountered a SQL execution error "
                    f"for {framework} at prediction CSV line "
                    f"{sql_error_match.group(1)}. Evaluation stopped before "
                    "complete results were produced; existing metrics, report, "
                    "and charts were not updated.\n"
                    f"Evaluator details:\n{evaluator_output}"
                )
            raise RuntimeError(
                f"The original evaluator failed for {framework} "
                f"(exit {completed.returncode}). Evaluation stopped before "
                "complete results were produced; existing metrics, report, "
                "and charts were not updated.\n"
                f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
            )

    correct_match = re.search(r"^Correct:\s*(\d+)/(\d+)\s*$", completed.stdout, re.M)
    accuracy_match = re.search(
        r"^Accuracy:\s*([0-9.]+)\s+\(([0-9.]+)%\)\s*$",
        completed.stdout,
        re.M,
    )
    if not correct_match or not accuracy_match:
        raise ValueError(
            f"Could not parse authoritative results from the original evaluator "
            f"for {framework}:\n{completed.stdout}"
        )

    correct = int(correct_match.group(1))
    total = int(correct_match.group(2))
    if total != EXPECTED_QUESTIONS:
        raise ValueError(
            f"The original evaluator processed {total} rows for {framework}; "
            f"expected {EXPECTED_QUESTIONS}."
        )
    accuracy = float(accuracy_match.group(1))
    accuracy_percent = float(accuracy_match.group(2))
    calculated_accuracy = correct / total
    if round(calculated_accuracy, 4) != accuracy or round(
        calculated_accuracy * 100, 2
    ) != accuracy_percent:
        raise ValueError(
            f"The original evaluator's printed accuracy disagrees with its "
            f"correct count for {framework}: {completed.stdout}"
        )
    return {
        "correct": correct,
        "accuracy": accuracy,
        "accuracy_percent": accuracy_percent,
        "evaluator_stdout": completed.stdout.strip(),
        "sql_execution_errors": 0,
    }


def evaluate_framework(framework, labels, rows):
    generated = sum(row["generation_status"] == "SUCCESS" for row in rows)
    failed_generations = len(rows) - generated
    times = []
    errors = []
    model_ids = {}
    for index, row in enumerate(rows, start=1):
        if row["generation_status"] != "SUCCESS":
            errors.append(
                {
                    "question_index": index,
                    "kind": "generation_failure",
                    "detail": row["error"],
                }
            )
        if row["generation_status"] == "SUCCESS" and row["model_id"]:
            model_ids[row["model_id"]] = model_ids.get(row["model_id"], 0) + 1
        if row["generation_status"] == "SUCCESS":
            try:
                generation_time = float(row["generation_time_seconds"])
                if generation_time >= 0:
                    times.append(generation_time)
            except (TypeError, ValueError):
                pass

    if failed_generations:
        raise RuntimeError(
            f"Cannot evaluate {framework}: {failed_generations} generation "
            "failure(s) are present. The original evaluator cannot count "
            "failed generations as incorrect answers. No new metrics, report, "
            "or charts were written.\n"
            + "\n".join(
                f"Q{error['question_index']}: {error['detail']}"
                for error in errors
            )
        )

    authoritative = run_teacher_evaluator(framework)

    return {
        "framework": framework,
        "total_questions": len(labels),
        "generated_successfully": generated,
        "correct": authoritative["correct"],
        "accuracy": authoritative["accuracy"],
        "accuracy_percent": authoritative["accuracy_percent"],
        "accuracy_source": TEACHER_EVALUATOR_PATH.name,
        "accuracy_source_output": authoritative["evaluator_stdout"],
        "mean_generation_time_seconds": mean(times) if times else None,
        "median_generation_time_seconds": median(times) if times else None,
        "timed_successful_generations": len(times),
        "failed_generations": failed_generations,
        "sql_execution_errors": authoritative["sql_execution_errors"],
        "sql_execution_errors_basis": (
            "Zero observed because the original evaluator completed all "
            f"{len(rows)} prediction queries successfully."
        ),
        "actual_model_ids": model_ids,
        "errors": errors,
    }


def svg_accuracy(metrics):
    width, height = 760, 390
    left, top, plot_width, plot_height = 80, 40, 620, 250
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<text x="380" y="24" text-anchor="middle" font-family="Arial" font-size="18" font-weight="bold">Exact-result accuracy by prompt framework</text>',
    ]
    for tick in range(0, 101, 20):
        y = top + plot_height * (100 - tick) / 100
        parts.extend(
            [
                f'<line x1="{left}" y1="{y:.1f}" x2="{left + plot_width}" y2="{y:.1f}" stroke="#d9e0e8"/>',
                f'<text x="{left - 12}" y="{y + 4:.1f}" text-anchor="end" font-family="Arial" font-size="12" fill="#445">{tick}%</text>',
            ]
        )

    colors = {"RTF": "#3b82f6", "ICIO": "#10b981", "CRISP": "#f59e0b"}
    bar_width, gap = 105, 85
    start_x = left + 55
    for index, item in enumerate(metrics):
        x = start_x + index * (bar_width + gap)
        accuracy = item["accuracy"] * 100
        bar_height = plot_height * accuracy / 100
        y = top + plot_height - bar_height
        parts.extend(
            [
                f'<rect x="{x}" y="{y:.1f}" width="{bar_width}" height="{bar_height:.1f}" rx="5" fill="{colors[item["framework"]]}"/>',
                f'<text x="{x + bar_width / 2}" y="{max(top + 15, y - 8):.1f}" text-anchor="middle" font-family="Arial" font-size="14" font-weight="bold">{accuracy:.1f}%</text>',
                f'<text x="{x + bar_width / 2}" y="{top + plot_height + 23}" text-anchor="middle" font-family="Arial" font-size="14">{html.escape(item["framework"])}</text>',
                f'<text x="{x + bar_width / 2}" y="{top + plot_height + 43}" text-anchor="middle" font-family="Arial" font-size="11" fill="#445">{item["correct"]}/{item["total_questions"]} correct</text>',
            ]
        )
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def svg_times(metrics):
    width, height = 760, 390
    left, top, plot_width, plot_height = 80, 45, 620, 245
    finite = [
        value
        for item in metrics
        for value in (
            item["mean_generation_time_seconds"],
            item["median_generation_time_seconds"],
        )
        if value is not None
    ]
    maximum = max(finite, default=1.0)
    maximum = max(maximum, 0.1) * 1.15
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<text x="380" y="24" text-anchor="middle" font-family="Arial" font-size="18" font-weight="bold">Generation time per completed response</text>',
    ]
    for tick in range(6):
        value = maximum * tick / 5
        y = top + plot_height * (1 - tick / 5)
        parts.extend(
            [
                f'<line x1="{left}" y1="{y:.1f}" x2="{left + plot_width}" y2="{y:.1f}" stroke="#d9e0e8"/>',
                f'<text x="{left - 10}" y="{y + 4:.1f}" text-anchor="end" font-family="Arial" font-size="11" fill="#445">{value:.1f}</text>',
            ]
        )
    group_width, group_gap = 120, 65
    start_x = left + 42
    for index, item in enumerate(metrics):
        x = start_x + index * (group_width + group_gap)
        for offset, key, color in (
            (12, "mean_generation_time_seconds", "#6366f1"),
            (65, "median_generation_time_seconds", "#14b8a6"),
        ):
            value = item[key]
            if value is None:
                continue
            bar_height = plot_height * value / maximum
            y = top + plot_height - bar_height
            parts.extend(
                [
                    f'<rect x="{x + offset}" y="{y:.1f}" width="40" height="{bar_height:.1f}" rx="4" fill="{color}"/>',
                    f'<text x="{x + offset + 20}" y="{max(top + 13, y - 6):.1f}" text-anchor="middle" font-family="Arial" font-size="10">{value:.2f}</text>',
                ]
            )
        parts.append(
            f'<text x="{x + 58}" y="{top + plot_height + 22}" text-anchor="middle" font-family="Arial" font-size="14">{html.escape(item["framework"])}</text>'
        )
    parts.extend(
        [
            '<rect x="245" y="347" width="13" height="13" fill="#6366f1"/><text x="264" y="358" font-family="Arial" font-size="12">Mean</text>',
            '<rect x="335" y="347" width="13" height="13" fill="#14b8a6"/><text x="354" y="358" font-family="Arial" font-size="12">Median</text>',
            '<text x="20" y="175" transform="rotate(-90 20 175)" text-anchor="middle" font-family="Arial" font-size="12">Seconds</text>',
            "</svg>",
        ]
    )
    return "\n".join(parts) + "\n"


def fmt_seconds(value):
    return "n/a" if value is None else f"{value:.3f}"


def write_report(metrics, metadata, differing_sql_questions):
    all_models = sorted(
        {
            model_id
            for item in metrics
            for model_id in item["actual_model_ids"]
        }
    )
    same_model = len(all_models) == 1
    model_status = (
        f"All successfully generated responses reported `{all_models[0]}`."
        if same_model and all_models
        else (
            "The actual model ID varied or was not reported across responses: "
            + (", ".join(f"`{model}`" for model in all_models) or "none")
            + "."
        )
    )
    session_rows = []
    for framework in FRAMEWORKS:
        session = metadata["sessions"][framework]
        model_ids = ", ".join(
            f"`{model}`" for model in session.get("actual_model_ids", [])
        ) or "none"
        session_rows.append(
            f"| {framework} | `{session['session_id']}` | "
            f"`{metadata['model_setting']}` | {model_ids} |"
        )

    table_rows = []
    for item in metrics:
        table_rows.append(
            "| {framework} | {total_questions} | {generated_successfully} | "
            "{correct} | {accuracy:.2%} | {mean_time} | {median_time} | "
            "{failed_generations} | {sql_execution_errors} |".format(
                **item,
                mean_time=fmt_seconds(item["mean_generation_time_seconds"]),
                median_time=fmt_seconds(item["median_generation_time_seconds"]),
            )
        )

    errors_summary = []
    for item in metrics:
        examples = [
            f"Q{error['question_index']}: {error['kind']} — {error['detail']}"
            for error in item["errors"][:5]
        ]
        if examples:
            errors_summary.append(
                f"- **{item['framework']}** ({len(item['errors'])} recorded issues): "
                + "; ".join(examples)
            )
        else:
            errors_summary.append(f"- **{item['framework']}**: none.")

    prior_results_match = all(
        item.get("prior_metrics_comparison", {}).get(
            "matches_previous_results", False
        )
        for item in metrics
    )
    prior_results_note = (
        "The authoritative evaluator results match the previously stored metrics "
        "for all three frameworks."
        if prior_results_match
        else (
            "At least one result differs from the previously stored metrics; "
            "see `data/task2_metrics.json` for the per-framework comparison."
        )
    )
    report = f"""# Task 2: Text-to-SQL Prompt Comparison

## Methodology

The benchmark contains {metrics[0]['total_questions']} original questions. Each framework was run in its own named GitHub Copilot CLI session, using the corresponding final Task 1 prompt as that session's custom-agent instructions. The original question text and ordering were retained. Reference results and database contents were not sent to the model. Each question was submitted once; no automatic retries were made. The generated SQL, framework, observed model ID, per-request generation time, status, error, and session ID are stored in the framework's CSV.

The authenticated official Copilot SDK model catalog returned only `auto`; the user approved proceeding with automatic routing. The configured model setting for all three sessions was `{metadata['model_setting']}`. Explicit selection of `gpt-6-luna` was not successfully set and was rejected by the CLI, so the model must not be described as pinned. The actual model ID returned with every assistant response was recorded. {model_status} All responses in this run therefore have the same observed model ID, but automatic routing does not guarantee that ID in future runs.

Generation latency is the interval between the CLI JSON event timestamp for the submitted question and the timestamp of the completed assistant response. CLI startup, dataset loading, and SQL evaluation are excluded. Mean and median generation times use successful generations with a parseable latency; failures are reported separately and are not assigned fabricated latency values.

## Results

Accuracy means **exact result-set accuracy**. It is taken from the unmodified instructor-provided `{TEACHER_EVALUATOR_PATH.name}` script, which executes each predicted query against the supplied SQLite data and compares rows as multisets (including duplicates). The evaluator was run separately for each framework in an isolated temporary directory containing copies of the required inputs; original datasets, predictions, and evaluator were not changed. The original evaluator stops with an error if a prediction cannot be executed, and it does not count failed generations or SQL execution errors as incorrect answers. This workflow therefore aborts without updating metrics, this report, or charts if generation failed or the evaluator encounters an SQL execution error. A reported SQL error count of zero means the original evaluator completed all prediction queries for that framework. Accuracy uses all {metrics[0]['total_questions']} benchmark questions as its denominator. {prior_results_note}

| Framework | Questions | Generated | Correct | Accuracy | Mean time (s) | Median time (s) | Failed generations | SQL execution errors observed |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
{chr(10).join(table_rows)}

![Exact-result accuracy by framework](data/task2_accuracy.svg)

![Mean and median generation time by framework](data/task2_generation_times.svg)

## Interpretation

"""
    if all(
        item["accuracy_percent"] == metrics[0]["accuracy_percent"]
        for item in metrics
    ):
        report += (
            "All three frameworks achieved the same measured accuracy on this "
            f"benchmark. Generated SQL text differed among frameworks on "
            f"{differing_sql_questions} of {metrics[0]['total_questions']} "
            "questions, but those variations did not change the aggregate "
            "correct count. The timing figures differ, but this one-run "
            "experiment does not establish that the differences are caused by "
            "prompt structure.\n\n"
        )
    else:
        best = max(metrics, key=lambda item: item["accuracy_percent"])
        report += (
            f"{best['framework']} had the highest measured accuracy "
            f"({best['accuracy_percent']:.2f}%). This is an observed difference on this "
            "benchmark, not by itself evidence of statistical significance or "
            "general superiority.\n\n"
        )
    fastest = [
        item for item in metrics if item["mean_generation_time_seconds"] is not None
    ]
    if fastest:
        quickest = min(fastest, key=lambda item: item["mean_generation_time_seconds"])
        report += (
            f"{quickest['framework']} had the lowest mean successful-response "
            f"latency ({quickest['mean_generation_time_seconds']:.3f} s). "
            "Timing reflects observed CLI response latency and may vary with "
            "network conditions, service load, and automatic model routing.\n\n"
        )
    if all(
        item["sql_execution_errors"] == 0
        and item["failed_generations"] == 0
        for item in metrics
    ):
        report += (
            f"All {metrics[0]['total_questions'] - metrics[0]['correct']} "
            "incorrect predictions were executable SQL result mismatches; "
            "the original evaluator completed every prediction query, so no "
            "SQL execution errors or failed generations were observed.\n\n"
        )

    report += f"""## Generation and SQL issues

"""
    report += "\n".join(errors_summary)
    report += f"""

## Sessions and model IDs

| Framework | Copilot session ID | Configured model setting | Observed model IDs |
|---|---|---|---|
{chr(10).join(session_rows)}

Session IDs, prompt hashes, CLI version, and model-selection notes are also stored in [`data/task2_experiment_metadata.json`](data/task2_experiment_metadata.json). Authoritative evaluator output and the comparison with previously stored metrics are recorded in [`data/task2_metrics.json`](data/task2_metrics.json). Prediction files are [`data/task2_predictions_rtf.csv`](data/task2_predictions_rtf.csv), [`data/task2_predictions_icio.csv`](data/task2_predictions_icio.csv), and [`data/task2_predictions_crisp.csv`](data/task2_predictions_crisp.csv).

## Limitations

- Auto routing (`auto`) was configured because the CLI model catalog did not expose a selectable specific model and explicit selection of `gpt-6-luna` was rejected. In this run, all 465 responses reported `gpt-6-luna`, so the observed model ID did not vary across the three sessions. The model was not pinned, and automatic routing does not guarantee the same model in future runs.
- The experiment uses one run per question and framework. It does not estimate run-to-run stochastic variation or establish statistical significance.
- The examples and task instructions constrain the model, but performance is specific to this benchmark, schema, database, and prompt wording.
- Generation failures and SQL execution errors are not automatically counted as incorrect by the original evaluator. The workflow stops and does not update final metrics, report, or charts unless the complete set of predictions can be evaluated. For this run, every generation succeeded and the evaluator completed all queries.
"""
    REPORT_PATH.write_text(report, encoding="utf-8")


def main():
    labels = read_labels()
    metadata = json.loads(METADATA_PATH.read_text(encoding="utf-8"))
    previous_metrics = {}
    if METRICS_PATH.is_file():
        previous_data = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
        previous_metrics = {
            item["framework"]: item
            for item in previous_data.get("metrics", [])
            if "framework" in item
        }
    metrics = []
    predictions_by_framework = {}
    for framework in FRAMEWORKS:
        rows = read_predictions(framework, labels)
        predictions_by_framework[framework] = rows
        item = evaluate_framework(framework, labels, rows)
        previous = previous_metrics.get(framework)
        if previous is not None:
            previous_accuracy_percent = round(
                float(previous["accuracy"]) * 100, 2
            )
            item["prior_metrics_comparison"] = {
                "previous_correct": previous.get("correct"),
                "previous_accuracy": previous.get("accuracy"),
                "matches_previous_results": (
                    previous.get("correct") == item["correct"]
                    and previous_accuracy_percent == item["accuracy_percent"]
                ),
            }
        metrics.append(item)

    differing_sql_questions = sum(
        len(
            {
                predictions_by_framework[framework][index]["predicted_sql"]
                for framework in FRAMEWORKS
            }
        )
        > 1
        for index in range(EXPECTED_QUESTIONS)
    )
    METRICS_PATH.write_text(
        json.dumps(
            {
                "evaluated_utc": datetime.now(timezone.utc).isoformat(),
                "accuracy_denominator": EXPECTED_QUESTIONS,
                "accuracy_evaluator": {
                    "file": TEACHER_EVALUATOR_PATH.name,
                    "sha256": hashlib.sha256(
                        TEACHER_EVALUATOR_PATH.read_bytes()
                    ).hexdigest(),
                    "authoritative": True,
                    "execution_method": (
                        "Original evaluator run in one isolated temporary "
                        "directory per framework with copied inputs."
                    ),
                },
                "metrics": metrics,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    (DATA_DIR / "task2_accuracy.svg").write_text(
        svg_accuracy(metrics), encoding="utf-8"
    )
    (DATA_DIR / "task2_generation_times.svg").write_text(
        svg_times(metrics), encoding="utf-8"
    )
    write_report(metrics, metadata, differing_sql_questions)

    print("Framework | Generated | Correct | Accuracy | Mean s | Median s | Failed")
    for item in metrics:
        print(
            f"{item['framework']} | {item['generated_successfully']} | "
            f"{item['correct']} | {item['accuracy']:.2%} | "
            f"{fmt_seconds(item['mean_generation_time_seconds'])} | "
            f"{fmt_seconds(item['median_generation_time_seconds'])} | "
            f"{item['failed_generations']}"
        )
    print("Report and charts written.")


if __name__ == "__main__":
    main()
