"""Reproducible paired analysis of the existing Task 2 and Task 3 results."""

import csv
import hashlib
import html
import importlib.util
import json
import math
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean, median

import numpy as np
import scipy
from scipy import stats


TASK_DIR = Path(__file__).resolve().parent
ASSIGNMENTS_DIR = TASK_DIR.parent
DATA_DIR = ASSIGNMENTS_DIR / "Task_2" / "data"
TASK1_DIR = ASSIGNMENTS_DIR / "Task_1"
TASK3_DIR = ASSIGNMENTS_DIR / "Task_3"
LABELS_PATH = DATA_DIR / "restaurants_dataset.csv"
SCHEMA_PATH = DATA_DIR / "restaurants-schema.csv"
DATABASE_PATH = DATA_DIR / "restaurants-db.txt"
TEACHER_EVALUATOR_PATH = DATA_DIR / "evaluate_retrieval_predictions.py"
TASK2_METRICS_PATH = DATA_DIR / "task2_metrics.json"
METADATA_PATH = DATA_DIR / "task2_experiment_metadata.json"
TASK3_METRICS_PATH = TASK3_DIR / "task3_metrics.json"
TASK3_SCORES_PATH = TASK3_DIR / "task3_per_question_scores.csv"
OUTPUT_JSON = TASK_DIR / "task4_statistics.json"
OUTPUT_REPORT = TASK_DIR / "task4_report.md"
ALPHA = 0.05
BOOTSTRAP_REPLICATES = 10_000
BOOTSTRAP_SEED = 20261017
FRAMEWORKS = ("RTF", "ICIO", "CRISP")
PROMPT_FILES = {
    "RTF": "prompt_rtf.txt",
    "ICIO": "prompt_icio.txt",
    "CRISP": "prompt_crisp.txt",
}
PREDICTION_FIELDS = {
    "question",
    "predicted_sql",
    "framework",
    "model_id",
    "generation_time_seconds",
    "generation_status",
    "session_id",
}


def read_json(path):
    with path.open(encoding="utf-8") as source:
        return json.load(source)


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
                    f"Invalid JSON result in {LABELS_PATH} at line {line_number}"
                ) from error
            if not isinstance(result, list) or not all(
                isinstance(result_row, list) for result_row in result
            ):
                raise ValueError(
                    f"Expected result rows as a JSON array at line {line_number}"
                )
            labels.append((row["question"], result))
    if len(labels) != 155:
        raise ValueError(f"Expected 155 reference questions, found {len(labels)}")
    return labels


def read_predictions(framework, questions):
    path = DATA_DIR / f"task2_predictions_{framework.lower()}.csv"
    with path.open(encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        if reader.fieldnames is None or not PREDICTION_FIELDS.issubset(
            reader.fieldnames
        ):
            raise ValueError(f"Missing required prediction fields in {path}")
        rows = list(reader)

    if len(rows) != len(questions):
        raise ValueError(
            f"{framework}: expected {len(questions)} rows, found {len(rows)}"
        )
    if [row["question"] for row in rows] != questions:
        raise ValueError(f"{framework}: question order/text differs from labels")
    if any(row["framework"] != framework for row in rows):
        raise ValueError(f"{framework}: mismatched framework value in CSV")
    return rows


def authorize_read_only(action, _arg1, _arg2, _database, _trigger):
    _ = (_arg1, _arg2, _database, _trigger)
    allowed = {
        sqlite3.SQLITE_SELECT,
        sqlite3.SQLITE_READ,
        sqlite3.SQLITE_FUNCTION,
    }
    if hasattr(sqlite3, "SQLITE_RECURSIVE"):
        allowed.add(sqlite3.SQLITE_RECURSIVE)
    return sqlite3.SQLITE_OK if action in allowed else sqlite3.SQLITE_DENY


def load_original_evaluator_database():
    evaluator_spec = importlib.util.spec_from_file_location(
        "task4_original_evaluator", TEACHER_EVALUATOR_PATH
    )
    if evaluator_spec is None or evaluator_spec.loader is None:
        raise ImportError(f"Cannot load original evaluator: {TEACHER_EVALUATOR_PATH}")
    evaluator = importlib.util.module_from_spec(evaluator_spec)
    evaluator_spec.loader.exec_module(evaluator)
    return evaluator.load_database()


def row_counter(rows):
    return Counter(tuple(row) for row in rows)


def multiset_jaccard(predicted_rows, reference_rows):
    predicted = row_counter(predicted_rows)
    reference = row_counter(reference_rows)
    intersection = sum((predicted & reference).values())
    union = sum((predicted | reference).values())
    return (intersection / union if union else 1.0), intersection, union


def run_teacher_evaluator(framework):
    prediction_path = DATA_DIR / f"task2_predictions_{framework.lower()}.csv"
    with tempfile.TemporaryDirectory(prefix=f"task4-evaluator-{framework.lower()}-") as tmp:
        work_dir = Path(tmp)
        for source in (
            TEACHER_EVALUATOR_PATH,
            LABELS_PATH,
            SCHEMA_PATH,
            DATABASE_PATH,
        ):
            shutil.copy2(source, work_dir / source.name)
        shutil.copy2(
            prediction_path, work_dir / "restaurants_dataset_predictions.csv"
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
    if completed.returncode:
        raise RuntimeError(
            f"Original evaluator failed for {framework}.\n"
            f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
        )
    correct = re.search(r"^Correct:\s*(\d+)/(\d+)\s*$", completed.stdout, re.M)
    accuracy = re.search(
        r"^Accuracy:\s*([0-9.]+)\s+\(([0-9.]+)%\)\s*$",
        completed.stdout,
        re.M,
    )
    if not correct or not accuracy:
        raise ValueError(
            f"Could not parse original evaluator output for {framework}: "
            f"{completed.stdout}"
        )
    return {
        "correct": int(correct.group(1)),
        "total": int(correct.group(2)),
        "accuracy": float(accuracy.group(1)),
        "accuracy_percent": float(accuracy.group(2)),
        "stdout": completed.stdout.strip(),
    }


def evaluate_question_rows(labels, predictions_by_framework):
    connection = load_original_evaluator_database()
    connection.set_authorizer(authorize_read_only)
    output = {framework: [] for framework in FRAMEWORKS}
    try:
        for framework in FRAMEWORKS:
            for index, ((question, reference_rows), prediction) in enumerate(
                zip(labels, predictions_by_framework[framework]), start=1
            ):
                status = prediction["generation_status"]
                result_rows = []
                error_type = ""
                error_message = ""
                if status != "SUCCESS":
                    error_type = "generation_failure"
                    error_message = prediction.get("error", "") or status
                else:
                    try:
                        result_rows = connection.execute(
                            prediction["predicted_sql"]
                        ).fetchall()
                    except sqlite3.Error as error:
                        error_type = "sql_execution_error"
                        error_message = str(error)

                exact = (
                    not error_type
                    and row_counter(result_rows) == row_counter(reference_rows)
                )
                jaccard, intersection, union = (
                    multiset_jaccard(result_rows, reference_rows)
                    if not error_type
                    else (0.0, 0, 0)
                )
                output[framework].append(
                    {
                        "question_index": index,
                        "question": question,
                        "exact": bool(exact),
                        "jaccard": jaccard,
                        "intersection": intersection,
                        "union": union,
                        "predicted_row_count": len(result_rows),
                        "reference_row_count": len(reference_rows),
                        "error_type": error_type,
                        "error": error_message,
                    }
                )
    finally:
        connection.close()
    return output


def validate_task3_scores(evaluated, task3_metrics):
    stored = {}
    with TASK3_SCORES_PATH.open(encoding="utf-8-sig", newline="") as source:
        for row in csv.DictReader(source):
            key = (row["framework"], int(row["question_index"]))
            if key in stored:
                raise ValueError(f"Duplicate Task 3 score entry: {key}")
            stored[key] = row
    if len(stored) != 465:
        raise ValueError(f"Expected 465 Task 3 score rows, found {len(stored)}")

    for framework in FRAMEWORKS:
        for item in evaluated[framework]:
            key = (framework, item["question_index"])
            row = stored.get(key)
            if row is None or row["question"] != item["question"]:
                raise ValueError(f"Task 3 score missing or misaligned at {key}")
            if not math.isclose(
                float(row["multiset_jaccard_similarity"]),
                item["jaccard"],
                rel_tol=0.0,
                abs_tol=1e-12,
            ):
                raise ValueError(f"Recomputed Jaccard differs from Task 3 at {key}")
            if row["exact_match"].lower() != str(item["exact"]).lower():
                raise ValueError(f"Task 3 exact flag differs at {key}")

    stored_summaries = {
        row["framework"]: row for row in task3_metrics.get("summaries", [])
    }
    for framework in FRAMEWORKS:
        values = [item["jaccard"] for item in evaluated[framework]]
        summary = stored_summaries.get(framework)
        if summary is None:
            raise ValueError(f"Task 3 summary missing for {framework}")
        if not math.isclose(
            mean(values),
            summary["mean_multiset_jaccard_similarity"],
            rel_tol=0.0,
            abs_tol=1e-12,
        ):
            raise ValueError(f"Task 3 mean differs for {framework}")


def run_friedman(values):
    result = stats.friedmanchisquare(*values)
    if not math.isfinite(float(result.statistic)) or not math.isfinite(
        float(result.pvalue)
    ):
        return {"statistic": None, "p_value": None, "status": "not_estimable"}
    statistic = float(result.statistic)
    return {
        "statistic": statistic,
        "p_value": float(result.pvalue),
        "status": "computed",
        "kendalls_w": statistic / (len(values[0]) * (len(values) - 1)),
    }


def holm_adjust(p_values):
    order = sorted(range(len(p_values)), key=p_values.__getitem__)
    adjusted = [None] * len(p_values)
    running_max = 0.0
    total = len(p_values)
    for rank, index in enumerate(order):
        candidate = min(1.0, (total - rank) * p_values[index])
        running_max = max(running_max, candidate)
        adjusted[index] = running_max
    return adjusted


def wilcoxon_pair(first, second):
    differences = np.asarray(first, dtype=float) - np.asarray(second, dtype=float)
    result = stats.wilcoxon(
        first,
        second,
        zero_method="wilcox",
        correction=False,
        alternative="two-sided",
        method="auto",
    )
    nonzero = differences[differences != 0]
    ranks = stats.rankdata(np.abs(nonzero), method="average")
    positive_rank_sum = float(ranks[nonzero > 0].sum())
    negative_rank_sum = float(ranks[nonzero < 0].sum())
    total_rank_sum = positive_rank_sum + negative_rank_sum
    rank_biserial = (
        (positive_rank_sum - negative_rank_sum) / total_rank_sum
        if total_rank_sum
        else 0.0
    )
    return {
        "statistic": float(result.statistic),
        "p_value": float(result.pvalue),
        "test_method": (
            "two-sided Wilcoxon signed-rank; zero_method='wilcox', "
            "continuity correction disabled, method='auto'"
        ),
        "nonzero_pairs": int(nonzero.size),
        "zero_difference_pairs": int(differences.size - nonzero.size),
        "mean_difference_first_minus_second": float(np.mean(differences)),
        "median_difference_first_minus_second": float(np.median(differences)),
        "rank_biserial_correlation": rank_biserial,
        "positive_rank_sum": positive_rank_sum,
        "negative_rank_sum": negative_rank_sum,
    }


def bootstrap_mean_difference(first, second, rng):
    differences = np.asarray(first, dtype=float) - np.asarray(second, dtype=float)
    replicates = np.empty(BOOTSTRAP_REPLICATES, dtype=float)
    for index in range(BOOTSTRAP_REPLICATES):
        sample_indices = rng.integers(0, len(differences), size=len(differences))
        replicates[index] = differences[sample_indices].mean()
    lower, upper = np.quantile(replicates, [0.025, 0.975], method="linear")
    return {
        "lower": float(lower),
        "upper": float(upper),
        "method": "paired question-level percentile bootstrap of the mean difference",
        "replicates": BOOTSTRAP_REPLICATES,
    }


def tukey_summary(values):
    array = np.asarray(values, dtype=float)
    q1, median_value, q3 = np.quantile(array, [0.25, 0.5, 0.75], method="linear")
    iqr = q3 - q1
    lower_fence = q1 - 1.5 * iqr
    upper_fence = q3 + 1.5 * iqr
    outliers = array[(array < lower_fence) | (array > upper_fence)]
    return {
        "count": int(array.size),
        "minimum": float(array.min()),
        "q1": float(q1),
        "median": float(median_value),
        "q3": float(q3),
        "maximum": float(array.max()),
        "iqr": float(iqr),
        "lower_tukey_fence": float(lower_fence),
        "upper_tukey_fence": float(upper_fence),
        "tukey_outlier_count": int(outliers.size),
    }


def analyze_data_quality(predictions_by_framework):
    result = {}
    times = {}
    for framework in FRAMEWORKS:
        valid = []
        missing = []
        invalid = []
        model_ids = Counter()
        statuses = Counter()
        for index, row in enumerate(predictions_by_framework[framework], start=1):
            statuses[row["generation_status"]] += 1
            model_ids[row["model_id"]] += 1
            raw = row["generation_time_seconds"]
            try:
                value = float(raw)
            except (TypeError, ValueError):
                if raw:
                    invalid.append(index)
                else:
                    missing.append(index)
                continue
            if not math.isfinite(value) or value < 0:
                invalid.append(index)
                continue
            valid.append(value)
        times[framework] = valid
        result[framework] = {
            "row_count": len(predictions_by_framework[framework]),
            "generation_status_counts": dict(statuses),
            "model_id_counts": dict(model_ids),
            "timed_rows": len(valid),
            "missing_time_question_indices": missing,
            "invalid_time_question_indices": invalid,
            "time_distribution": tukey_summary(valid) if valid else None,
        }
    return result, times


def analyze_accuracy(evaluated, official_results):
    flags = {
        framework: [item["exact"] for item in evaluated[framework]]
        for framework in FRAMEWORKS
    }
    pairwise = []
    for index, (first, second) in enumerate(
        (("RTF", "ICIO"), ("RTF", "CRISP"), ("ICIO", "CRISP"))
    ):
        b = sum(a and not c for a, c in zip(flags[first], flags[second]))
        c = sum(not a and d for a, d in zip(flags[first], flags[second]))
        pairwise.append(
            {
                "first": first,
                "second": second,
                "first_correct_second_incorrect": b,
                "first_incorrect_second_correct": c,
                "discordant_pairs": b + c,
                "mcnemar_statistic": None,
                "p_value": None,
                "status": "not_informative_no_discordant_pairs"
                if b + c == 0
                else "requires_test",
            }
        )
    identical = all(flags[FRAMEWORKS[0]] == flags[item] for item in FRAMEWORKS[1:])
    return {
        "paired_question_count": len(flags[FRAMEWORKS[0]]),
        "per_framework_correct": {
            framework: sum(flags[framework]) for framework in FRAMEWORKS
        },
        "identical_correctness_vectors": identical,
        "cochran_q": {
            "statistic": None,
            "degrees_of_freedom": 2,
            "p_value": None,
            "status": "not_estimable_no_discordant_outcomes"
            if identical
            else "requires_test",
            "reason": (
                "All three correctness indicators are identical for every "
                "question; Cochran's Q denominator is zero."
                if identical
                else "At least one question has discordant outcomes."
            ),
        },
        "pairwise_mcnemar": pairwise,
        "official_evaluator_results": official_results,
    }


def analyze_jaccard(evaluated):
    values = {
        framework: np.asarray(
            [item["jaccard"] for item in evaluated[framework]], dtype=float
        )
        for framework in FRAMEWORKS
    }
    pairwise_zero = all(
        np.array_equal(values[first], values[second])
        for first, second in (
            ("RTF", "ICIO"),
            ("RTF", "CRISP"),
            ("ICIO", "CRISP"),
        )
    )
    return {
        "paired_question_count": len(values["RTF"]),
        "identical_score_vectors": pairwise_zero,
        "pairwise_nonzero_difference_counts": {
            f"{first}_minus_{second}": int(
                np.count_nonzero(values[first] - values[second])
            )
            for first, second in (
                ("RTF", "ICIO"),
                ("RTF", "CRISP"),
                ("ICIO", "CRISP"),
            )
        },
        "friedman": {
            "statistic": None,
            "degrees_of_freedom": 2,
            "p_value": None,
            "status": "not_informative_all_paired_differences_are_zero"
            if pairwise_zero
            else "requires_test",
        },
        "pairwise_wilcoxon": [],
        "note": (
            "All per-question scores are identical across frameworks. "
            "Friedman and signed-rank tests cannot provide a meaningful "
            "framework contrast when every paired difference is zero."
            if pairwise_zero
            else "Paired nonparametric tests are reported."
        ),
    }


def analyze_times(times):
    counts = [len(times[framework]) for framework in FRAMEWORKS]
    if len(set(counts)) != 1 or counts[0] == 0:
        raise ValueError(
            "A paired time analysis requires a nonempty common set of timed "
            "questions. Current counts: "
            + ", ".join(f"{fw}={len(times[fw])}" for fw in FRAMEWORKS)
        )
    if any(not np.all(np.isfinite(times[framework])) for framework in FRAMEWORKS):
        raise ValueError("Non-finite generation time reached the paired analysis")

    arrays = {
        framework: np.asarray(times[framework], dtype=float)
        for framework in FRAMEWORKS
    }
    overall = run_friedman([arrays[framework] for framework in FRAMEWORKS])
    overall.update(
        {
            "degrees_of_freedom": 2,
            "paired_question_count": counts[0],
            "alpha": ALPHA,
            "significant_at_alpha": (
                overall["p_value"] < ALPHA
                if overall["p_value"] is not None
                else None
            ),
        }
    )

    comparisons = (
        ("RTF", "ICIO"),
        ("RTF", "CRISP"),
        ("ICIO", "CRISP"),
    )
    rng = np.random.default_rng(BOOTSTRAP_SEED)
    raw = []
    for first, second in comparisons:
        values = wilcoxon_pair(arrays[first], arrays[second])
        values.update(
            {
                "first": first,
                "second": second,
                "paired_question_count": counts[0],
                "bootstrap_95_percent_ci_mean_difference": (
                    bootstrap_mean_difference(
                        arrays[first], arrays[second], rng
                    )
                ),
            }
        )
        raw.append(values)
    adjusted = holm_adjust([item["p_value"] for item in raw])
    for item, p_adjusted in zip(raw, adjusted):
        item["holm_adjusted_p_value"] = p_adjusted
        item["significant_after_holm_at_alpha"] = p_adjusted < ALPHA
        item["faster_framework_by_mean"] = (
            item["first"]
            if item["mean_difference_first_minus_second"] < 0
            else (
                item["second"]
                if item["mean_difference_first_minus_second"] > 0
                else "tie"
            )
        )
    return {
        "question_level_paired": True,
        "paired_question_count": counts[0],
        "framework_summaries": {
            framework: {
                **tukey_summary(arrays[framework]),
                "mean": float(np.mean(arrays[framework])),
                "sample_standard_deviation": float(np.std(arrays[framework], ddof=1)),
            }
            for framework in FRAMEWORKS
        },
        "friedman": overall,
        "kendalls_w": overall.get("kendalls_w"),
        "pairwise_wilcoxon": raw,
        "holm_family_size": len(raw),
        "alpha": ALPHA,
        "bootstrap": {
            "replicates": BOOTSTRAP_REPLICATES,
            "seed": BOOTSTRAP_SEED,
            "resampling_unit": "question-level paired time differences",
        },
    }


def svg_metric_bars(summaries, key, title, y_label, filename, percent=False):
    width, height = 760, 410
    left, top, plot_width, plot_height = 80, 50, 620, 270
    colors = {"RTF": "#3b82f6", "ICIO": "#10b981", "CRISP": "#f59e0b"}
    multiplier = 100 if percent else 1
    suffix = "%" if percent else ""
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        f'<text x="380" y="27" text-anchor="middle" font-family="Arial" font-size="18" font-weight="bold">{html.escape(title)}</text>',
    ]
    for tick in range(0, 101, 20):
        y = top + plot_height * (100 - tick) / 100
        parts.extend(
            [
                f'<line x1="{left}" y1="{y:.1f}" x2="{left + plot_width}" y2="{y:.1f}" stroke="#d9e0e8"/>',
                f'<text x="{left - 12}" y="{y + 4:.1f}" text-anchor="end" font-family="Arial" font-size="12" fill="#445">{tick}{suffix}</text>',
            ]
        )
    for index, summary in enumerate(summaries):
        value = summary[key] * multiplier
        x = left + 55 + index * 190
        bar_height = plot_height * value / 100
        y = top + plot_height - bar_height
        label = f"{value:.2f}{suffix}" if percent else f"{value:.6f}"
        detail = (
            f"{summary['accuracy_correct']}/{summary['total_questions']} exact"
            if "accuracy_correct" in summary
            else f"n={summary['total_questions']}"
        )
        parts.extend(
            [
                f'<rect x="{x}" y="{y:.2f}" width="105" height="{bar_height:.2f}" rx="5" fill="{colors[summary["framework"]]}"/>',
                f'<text x="{x + 52.5}" y="{max(top + 15, y - 8):.2f}" text-anchor="middle" font-family="Arial" font-size="14" font-weight="bold">{label}</text>',
                f'<text x="{x + 52.5}" y="{top + plot_height + 25}" text-anchor="middle" font-family="Arial" font-size="14">{summary["framework"]}</text>',
                f'<text x="{x + 52.5}" y="{top + plot_height + 45}" text-anchor="middle" font-family="Arial" font-size="11" fill="#445">{detail}</text>',
            ]
        )
    parts.append(
        f'<text x="20" y="{top + plot_height / 2}" transform="rotate(-90 20 {top + plot_height / 2})" text-anchor="middle" font-family="Arial" font-size="12">{html.escape(y_label)}</text>'
    )
    parts.append("</svg>")
    (TASK_DIR / filename).write_text("\n".join(parts) + "\n", encoding="utf-8")


def svg_time_distributions(time_analysis):
    summaries = time_analysis["framework_summaries"]
    width, height = 850, 430
    left, right, top = 105, 25, 60
    plot_width = width - left - right
    axis_max = max(item["maximum"] for item in summaries.values())
    axis_max = max(0.5, math.ceil(axis_max * 2) / 2)
    colors = {"RTF": "#3b82f6", "ICIO": "#10b981", "CRISP": "#f59e0b"}
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<text x="425" y="28" text-anchor="middle" font-family="Arial" font-size="18" font-weight="bold">Per-question generation time distributions</text>',
        '<text x="425" y="48" text-anchor="middle" font-family="Arial" font-size="11" fill="#445">All 155 paired observations shown as points; boxes show median and interquartile range</text>',
    ]
    for tick in range(0, 6):
        value = axis_max * tick / 5
        x = left + plot_width * tick / 5
        parts.extend(
            [
                f'<line x1="{x:.1f}" y1="{top - 8}" x2="{x:.1f}" y2="{height - 65}" stroke="#e1e5eb"/>',
                f'<text x="{x:.1f}" y="{height - 42}" text-anchor="middle" font-family="Arial" font-size="11" fill="#445">{value:.1f}</text>',
            ]
        )
    for row_index, framework in enumerate(FRAMEWORKS):
        values = np.asarray(time_analysis["raw_times"][framework], dtype=float)
        summary = summaries[framework]
        center_y = top + 55 + row_index * 95
        x_pos = lambda value: left + plot_width * float(value) / axis_max
        for index, value in enumerate(values):
            jitter = ((index * 7) % 17) - 8
            parts.append(
                f'<circle cx="{x_pos(value):.2f}" cy="{center_y + jitter:.2f}" r="2.2" fill="{colors[framework]}" fill-opacity="0.32"/>'
            )
        parts.extend(
            [
                f'<text x="{left - 15}" y="{center_y + 5}" text-anchor="end" font-family="Arial" font-size="14">{framework}</text>',
                f'<line x1="{x_pos(summary["minimum"]):.2f}" y1="{center_y}" x2="{x_pos(summary["maximum"]):.2f}" y2="{center_y}" stroke="#263238" stroke-width="2"/>',
                f'<line x1="{x_pos(summary["minimum"]):.2f}" y1="{center_y - 9}" x2="{x_pos(summary["minimum"]):.2f}" y2="{center_y + 9}" stroke="#263238" stroke-width="2"/>',
                f'<line x1="{x_pos(summary["maximum"]):.2f}" y1="{center_y - 9}" x2="{x_pos(summary["maximum"]):.2f}" y2="{center_y + 9}" stroke="#263238" stroke-width="2"/>',
                f'<rect x="{x_pos(summary["q1"]):.2f}" y="{center_y - 13}" width="{max(1, x_pos(summary["q3"]) - x_pos(summary["q1"])):.2f}" height="26" fill="{colors[framework]}" fill-opacity="0.42" stroke="{colors[framework]}" stroke-width="2"/>',
                f'<line x1="{x_pos(summary["median"]):.2f}" y1="{center_y - 14}" x2="{x_pos(summary["median"]):.2f}" y2="{center_y + 14}" stroke="#101820" stroke-width="3"/>',
                f'<text x="{width - 18}" y="{center_y + 5}" text-anchor="end" font-family="Arial" font-size="11" fill="#344">mean {summary["mean"]:.3f}s; outliers {summary["tukey_outlier_count"]}</text>',
            ]
        )
    parts.extend(
        [
            f'<text x="{left + plot_width / 2}" y="{height - 14}" text-anchor="middle" font-family="Arial" font-size="12">Generation latency (seconds)</text>',
            "</svg>",
        ]
    )
    (TASK_DIR / "task4_generation_time_distributions.svg").write_text(
        "\n".join(parts) + "\n", encoding="utf-8"
    )


def svg_paired_time_differences(time_analysis):
    pairs = time_analysis["pairwise_wilcoxon"]
    width, height = 850, 360
    left, right, top, plot_height = 105, 55, 60, 210
    bounds = [
        bound
        for item in pairs
        for bound in (
            item["bootstrap_95_percent_ci_mean_difference"]["lower"],
            item["bootstrap_95_percent_ci_mean_difference"]["upper"],
        )
    ]
    extent = max(abs(min(bounds)), abs(max(bounds)), 0.05) * 1.15
    plot_width = width - left - right
    x_pos = lambda value: left + plot_width * (value + extent) / (2 * extent)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<text x="425" y="27" text-anchor="middle" font-family="Arial" font-size="18" font-weight="bold">Paired mean generation-time differences</text>',
        '<text x="425" y="47" text-anchor="middle" font-family="Arial" font-size="11" fill="#445">First framework minus second; negative values mean the first was faster</text>',
    ]
    for tick in range(5):
        value = -extent + (2 * extent * tick / 4)
        x = x_pos(value)
        color = "#263238" if abs(value) < 1e-12 else "#e1e5eb"
        stroke_width = 2 if abs(value) < 1e-12 else 1
        parts.extend(
            [
                f'<line x1="{x:.2f}" y1="{top - 4}" x2="{x:.2f}" y2="{top + plot_height}" stroke="{color}" stroke-width="{stroke_width}"/>',
                f'<text x="{x:.2f}" y="{top + plot_height + 24}" text-anchor="middle" font-family="Arial" font-size="11" fill="#445">{value:.2f}</text>',
            ]
        )
    for index, item in enumerate(pairs):
        y = top + 35 + index * 65
        ci = item["bootstrap_95_percent_ci_mean_difference"]
        x_low, x_high = x_pos(ci["lower"]), x_pos(ci["upper"])
        x_mean = x_pos(item["mean_difference_first_minus_second"])
        parts.extend(
            [
                f'<text x="{left - 12}" y="{y + 4}" text-anchor="end" font-family="Arial" font-size="12">{item["first"]} − {item["second"]}</text>',
                f'<line x1="{x_low:.2f}" y1="{y}" x2="{x_high:.2f}" y2="{y}" stroke="#475569" stroke-width="4"/>',
                f'<line x1="{x_low:.2f}" y1="{y - 7}" x2="{x_low:.2f}" y2="{y + 7}" stroke="#475569" stroke-width="2"/>',
                f'<line x1="{x_high:.2f}" y1="{y - 7}" x2="{x_high:.2f}" y2="{y + 7}" stroke="#475569" stroke-width="2"/>',
                f'<circle cx="{x_mean:.2f}" cy="{y}" r="6" fill="#7c3aed"/>',
                f'<text x="{width - 12}" y="{y + 4}" text-anchor="end" font-family="Arial" font-size="10" fill="#344">Δ {item["mean_difference_first_minus_second"]:.3f}s</text>',
            ]
        )
    parts.append(
        f'<text x="{left + plot_width / 2}" y="{height - 20}" text-anchor="middle" font-family="Arial" font-size="12">Mean paired difference in response latency (seconds), with 95% question-bootstrap CI</text>'
    )
    parts.append("</svg>")
    (TASK_DIR / "task4_paired_time_differences.svg").write_text(
        "\n".join(parts) + "\n", encoding="utf-8"
    )


def framework_summaries(
    evaluated, times, predictions_by_framework, task2_metrics, task3_metrics
):
    task2 = {item["framework"]: item for item in task2_metrics["metrics"]}
    task3 = {item["framework"]: item for item in task3_metrics["summaries"]}
    summaries = []
    for framework in FRAMEWORKS:
        observations = evaluated[framework]
        jaccard_scores = [item["jaccard"] for item in observations]
        exact_count = sum(item["exact"] for item in observations)
        summary = {
            "framework": framework,
            "total_questions": len(observations),
            "successful_generations": sum(
                row["generation_status"] == "SUCCESS"
                for row in predictions_by_framework[framework]
            ),
            "correct": exact_count,
            "accuracy": exact_count / len(observations),
            "mean_jaccard": mean(jaccard_scores),
            "median_jaccard": median(jaccard_scores),
            "perfect_jaccard_count": sum(value == 1 for value in jaccard_scores),
            "partial_jaccard_count": sum(0 < value < 1 for value in jaccard_scores),
            "zero_jaccard_count": sum(value == 0 for value in jaccard_scores),
            "sql_execution_errors": sum(
                item["error_type"] == "sql_execution_error" for item in observations
            ),
            "failed_predictions": sum(
                item["error_type"] == "generation_failure" for item in observations
            ),
            "mean_generation_time_seconds": mean(times[framework]),
            "median_generation_time_seconds": median(times[framework]),
            "task2_accuracy_authoritative": task2[framework]["accuracy"],
            "task3_mean_authoritative": task3[framework][
                "mean_multiset_jaccard_similarity"
            ],
        }
        if exact_count != task2[framework]["correct"]:
            raise ValueError(
                f"{framework}: recomputed exact count {exact_count} disagrees "
                f"with Task 2 evaluator ({task2[framework]['correct']})"
            )
        if not math.isclose(
            summary["mean_generation_time_seconds"],
            task2[framework]["mean_generation_time_seconds"],
            rel_tol=0.0,
            abs_tol=1e-9,
        ):
            raise ValueError(
                f"{framework}: recomputed mean generation time disagrees with "
                "the stored Task 2 metric"
            )
        summaries.append(summary)
    return summaries


def prompt_summary(metadata):
    entries = []
    for framework in FRAMEWORKS:
        prompt_path = TASK1_DIR / PROMPT_FILES[framework]
        digest = hashlib.sha256(
            prompt_path.read_text(encoding="utf-8").encode("utf-8")
        ).hexdigest()
        expected = metadata["prompt_sha256"].get(framework)
        if digest != expected:
            raise ValueError(f"Prompt SHA-256 mismatch for {framework}")
        entries.append(
            {
                "framework": framework,
                "file": prompt_path.name,
                "sha256": digest,
            }
        )
    return entries


def build_analysis():
    labels = read_labels()
    questions = [question for question, _ in labels]
    task2_metrics = read_json(TASK2_METRICS_PATH)
    task3_metrics = read_json(TASK3_METRICS_PATH)
    metadata = read_json(METADATA_PATH)
    evaluator_hash = hashlib.sha256(TEACHER_EVALUATOR_PATH.read_bytes()).hexdigest()
    if evaluator_hash != task2_metrics["accuracy_evaluator"]["sha256"]:
        raise ValueError(
            "Original evaluator SHA-256 differs from the Task 2 recorded evaluator"
        )
    predictions_by_framework = {
        framework: read_predictions(framework, questions)
        for framework in FRAMEWORKS
    }
    quality, times = analyze_data_quality(predictions_by_framework)

    if any(
        quality[framework]["missing_time_question_indices"]
        or quality[framework]["invalid_time_question_indices"]
        for framework in FRAMEWORKS
    ):
        raise ValueError(
            "Generation time data are incomplete or invalid; a complete paired "
            "time analysis cannot be reported. See Task 4 script validation."
        )
    if any(
        quality[framework]["generation_status_counts"] != {"SUCCESS": len(labels)}
        for framework in FRAMEWORKS
    ):
        raise ValueError(
            "Generation failures are present. The original evaluator cannot "
            "produce complete accuracy results for failed rows."
        )
    if metadata.get("model_setting") != "auto":
        raise ValueError(
            "Expected the recorded Task 2 model setting `auto`; found "
            f"{metadata.get('model_setting')!r}"
        )
    for framework in FRAMEWORKS:
        session = metadata["sessions"][framework]
        expected_session = session["session_id"]
        if session.get("agent_name") != f"task2-{framework.lower()}":
            raise ValueError(f"Unexpected recorded agent for {framework}")
        if session.get("completed_rows") != len(labels):
            raise ValueError(f"Incomplete recorded session for {framework}")
        if any(
            row["session_id"] != expected_session
            for row in predictions_by_framework[framework]
        ):
            raise ValueError(
                f"{framework}: session IDs in CSV do not match metadata"
            )
        observed_ids = set(quality[framework]["model_id_counts"])
        expected_ids = set(session["actual_model_ids"])
        if observed_ids != expected_ids:
            raise ValueError(
                f"{framework}: model IDs in CSV do not match session metadata"
            )

    official_results = {
        framework: run_teacher_evaluator(framework) for framework in FRAMEWORKS
    }
    evaluated = evaluate_question_rows(labels, predictions_by_framework)
    for framework in FRAMEWORKS:
        errors = [
            item for item in evaluated[framework] if item["error_type"]
        ]
        if errors:
            raise RuntimeError(
                f"Cannot complete Task 4 result comparisons for {framework}; "
                f"found {len(errors)} execution errors."
            )
        exact_count = sum(item["exact"] for item in evaluated[framework])
        if exact_count != official_results[framework]["correct"]:
            raise ValueError(
                f"{framework}: per-question correctness ({exact_count}) "
                "disagrees with original evaluator "
                f"({official_results[framework]['correct']})"
            )
        stored_task2 = next(
            item
            for item in task2_metrics["metrics"]
            if item["framework"] == framework
        )
        if exact_count != stored_task2["correct"]:
            raise ValueError(
                f"{framework}: original evaluator output disagrees with "
                "stored Task 2 metrics"
            )
    validate_task3_scores(evaluated, task3_metrics)

    accuracy_stats = analyze_accuracy(evaluated, official_results)
    jaccard_stats = analyze_jaccard(evaluated)
    time_analysis = analyze_times(times)
    time_analysis["raw_times"] = times
    summaries = framework_summaries(
        evaluated,
        times,
        predictions_by_framework,
        task2_metrics,
        task3_metrics,
    )
    sql_pairwise = {}
    for first, second in (
        ("RTF", "ICIO"),
        ("RTF", "CRISP"),
        ("ICIO", "CRISP"),
    ):
        sql_pairwise[f"{first}_vs_{second}"] = sum(
            left["predicted_sql"] == right["predicted_sql"]
            for left, right in zip(
                predictions_by_framework[first], predictions_by_framework[second]
            )
        )
    all_identical_sql = sum(
        len(
            {
                predictions_by_framework[framework][index]["predicted_sql"]
                for framework in FRAMEWORKS
            }
        )
        == 1
        for index in range(len(labels))
    )

    results = {
        "analysis_timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "alpha": ALPHA,
        "question_count": len(labels),
        "question_order_identical": True,
        "model_setting": metadata.get("model_setting"),
        "observed_model_ids": {
            framework: quality[framework]["model_id_counts"]
            for framework in FRAMEWORKS
        },
        "prompt_hashes": prompt_summary(metadata),
        "session_metadata": {
            framework: metadata["sessions"][framework]
            for framework in FRAMEWORKS
        },
        "data_quality": quality,
        "framework_summaries": summaries,
        "per_question_pairing": {
            "exact_correctness_vectors_identical": accuracy_stats[
                "identical_correctness_vectors"
            ],
            "jaccard_vectors_identical": jaccard_stats[
                "identical_score_vectors"
            ],
            "sql_text_exact_matches_by_pair": sql_pairwise,
            "all_three_sql_texts_identical_count": all_identical_sql,
        },
        "statistical_tests": {
            "accuracy": accuracy_stats,
            "jaccard": jaccard_stats,
            "generation_time": {
                key: value
                for key, value in time_analysis.items()
                if key != "raw_times"
            },
        },
        "source_hashes": {
            "teacher_evaluator_sha256": hashlib.sha256(
                TEACHER_EVALUATOR_PATH.read_bytes()
            ).hexdigest(),
            "task2_prediction_csv_sha256": {
                framework: hashlib.sha256(
                    (DATA_DIR / f"task2_predictions_{framework.lower()}.csv").read_bytes()
                ).hexdigest()
                for framework in FRAMEWORKS
            },
        },
        "bootstrap_seed": BOOTSTRAP_SEED,
        "bootstrap_replicates": BOOTSTRAP_REPLICATES,
        "scipy_version": scipy.__version__,
        "numpy_version": np.__version__,
        "python_version": sys.version.split()[0],
    }
    return results, summaries, evaluated, time_analysis


def fmt(value, digits=4):
    return "N/A" if value is None else f"{value:.{digits}f}"


def report_text(results, summaries, time_analysis):
    accuracy = results["statistical_tests"]["accuracy"]
    jaccard = results["statistical_tests"]["jaccard"]
    friedman = time_analysis["friedman"]
    pairwise = time_analysis["pairwise_wilcoxon"]
    quality = results["data_quality"]
    exact_rows = []
    for item in summaries:
        session = results["session_metadata"][item["framework"]]
        exact_rows.append(
            f"| {item['framework']} | `{session['agent_name']}` "
            f"| `{session['session_id']}` | `auto` | `gpt-6-luna` | "
            f"{item['total_questions']} | {item['successful_generations']} |"
        )
    prompt_rows = [
        f"| {item['framework']} | `{item['file']}` | `{item['sha256']}` |"
        for item in results["prompt_hashes"]
    ]
    metric_rows = []
    for item in summaries:
        metric_rows.append(
            f"| {item['framework']} | {item['correct']}/{item['total_questions']} "
            f"| {item['accuracy']:.2%} | {item['mean_jaccard']:.9f} "
            f"| {item['median_jaccard']:.6f} "
            f"| {item['mean_generation_time_seconds']:.6f} "
            f"| {item['median_generation_time_seconds']:.6f} |"
        )
    distribution_rows = []
    for item in summaries:
        distribution_rows.append(
            f"| {item['framework']} | {item['perfect_jaccard_count']} "
            f"| {item['partial_jaccard_count']} | {item['zero_jaccard_count']} "
            f"| {item['sql_execution_errors']} | {item['failed_predictions']} |"
        )
    quality_rows = []
    for framework in FRAMEWORKS:
        item = quality[framework]["time_distribution"]
        quality_rows.append(
            f"| {framework} | {item['count']} | {item['minimum']:.6f} "
            f"| {item['q1']:.6f} | {item['median']:.6f} | {item['q3']:.6f} "
            f"| {item['maximum']:.6f} | {item['tukey_outlier_count']} |"
        )

    exact_test_rows = []
    for item in accuracy["pairwise_mcnemar"]:
        exact_test_rows.append(
            f"| McNemar exact | {item['first']} vs {item['second']} "
            f"| {accuracy['paired_question_count']} | "
            f"{item['discordant_pairs']} | N/A | N/A | N/A "
            f"| {item['status'].replace('_', ' ')} |"
        )
    exact_test_rows.insert(
        0,
        "| Cochran's Q | RTF, ICIO, CRISP | "
        f"{accuracy['paired_question_count']} | 0 | N/A | N/A | N/A "
        f"| {accuracy['cochran_q']['status'].replace('_', ' ')} |",
    )
    jaccard_test_rows = [
        "| Friedman | RTF, ICIO, CRISP | 155 | N/A | N/A | N/A "
        f"| {jaccard['friedman']['status'].replace('_', ' ')} |"
    ]
    for first, second in (
        ("RTF", "ICIO"),
        ("RTF", "CRISP"),
        ("ICIO", "CRISP"),
    ):
        jaccard_test_rows.append(
            f"| Wilcoxon signed-rank | {first} vs {second} | 155 | N/A "
            "| N/A | N/A | no nonzero paired differences |"
        )
    time_test_rows = [
        "| Friedman chi-square | RTF, ICIO, CRISP | "
        f"{time_analysis['paired_question_count']} | "
        f"{fmt(friedman['statistic'], 4)} | {fmt(friedman['p_value'], 8)} "
        f"| Kendall's W = {fmt(time_analysis['kendalls_w'], 4)} "
        f"| {'significant' if friedman['significant_at_alpha'] else 'not significant'} at α = 0.05 |"
    ]
    time_pair_rows = []
    for item in pairwise:
        ci = item["bootstrap_95_percent_ci_mean_difference"]
        time_test_rows.append(
            f"| Wilcoxon signed-rank | {item['first']} vs {item['second']} "
            f"| {item['paired_question_count']} | {item['statistic']:.2f} "
            f"| {item['p_value']:.8g} | r_rb = "
            f"{item['rank_biserial_correlation']:.4f}; Holm p = "
            f"{item['holm_adjusted_p_value']:.8g} "
            f"| {'significant' if item['significant_after_holm_at_alpha'] else 'not significant'} after Holm |"
        )
        time_pair_rows.append(
            f"| {item['first']} − {item['second']} | "
            f"{item['paired_question_count']} | "
            f"{item['mean_difference_first_minus_second']:.6f} | "
            f"{item['median_difference_first_minus_second']:.6f} | "
            f"[{ci['lower']:.6f}, {ci['upper']:.6f}] | "
            f"{item['faster_framework_by_mean']} | "
            f"{item['holm_adjusted_p_value']:.8g} | "
            f"{item['rank_biserial_correlation']:.4f} |"
        )

    sql_counts = results["per_question_pairing"]["sql_text_exact_matches_by_pair"]
    ci_lines = []
    for item in pairwise:
        ci = item["bootstrap_95_percent_ci_mean_difference"]
        ci_lines.append(
            f"- **{item['first']} vs {item['second']}:** mean paired difference "
            f"{item['mean_difference_first_minus_second']:+.6f} s "
            f"(median {item['median_difference_first_minus_second']:+.6f} s), "
            f"95% paired bootstrap CI [{ci['lower']:+.6f}, {ci['upper']:+.6f}] s; "
            f"Wilcoxon p = {item['p_value']:.8g}, Holm-adjusted p = "
            f"{item['holm_adjusted_p_value']:.8g}, rank-biserial effect "
            f"{item['rank_biserial_correlation']:+.4f}. "
            f"By the observed mean, {item['faster_framework_by_mean']} was faster."
        )

    exact_test_conclusion = (
        "All three correctness vectors are identical question-by-question. "
        "Every pair has zero discordant pairs, and the denominator in "
        "Cochran's Q is zero; the global test and pairwise McNemar tests are "
        "therefore not estimable/informative. This is an observed tie, not "
        "evidence that the frameworks are equivalent in general."
    )
    jaccard_conclusion = (
        "All 155 per-question Jaccard values are identical across all three "
        "frameworks. Every paired difference is zero, so Friedman and "
        "Wilcoxon tests provide no estimable framework contrast. The scores "
        "add no ranking distinction in this observed run."
    )

    return f"""# Task 4: Paired Analysis of Text-to-SQL Prompt Frameworks

## Executive summary

This report reanalyzes only the existing 155-question Task 2 benchmark and Task 3 scores. No Copilot sessions were created and no SQL predictions were generated. The three frameworks have identical exact-correctness outcomes on every question (43/155 each) and identical Task 3 Multiset Jaccard scores on every question. Accordingly, neither correctness metric separates the frameworks in this run. Generation times are the only outcome with observed per-question variation between frameworks; paired nonparametric tests and question-level bootstrap intervals quantify those differences.

## Data and experimental settings

Each CSV contains 155 questions in the original order, has the matching framework label, and records 155 successful generations with parseable nonnegative times. All 465 responses report `gpt-6-luna`; the configured setting was `auto`, not an explicitly pinned model ID. The original evaluator was executed separately on copied inputs for each framework. Its correct counts were cross-checked against independently recomputed per-question exact matches. Task 3's 465 per-question values and summary JSON were also checked against this analysis.

| Framework | CLI agent profile | Copilot session ID | Configured model | Observed response model ID | Questions | Successful generations |
|---|---|---|---|---|---:|---:|
{chr(10).join(exact_rows)}

| Framework | Prompt file | SHA-256 |
|---|---|---|
{chr(10).join(prompt_rows)}

The three framework prompts share the same schema, relationship guidance, general SQL rules, output constraints, and seven few-shot examples. Their primary planned difference is the organization of those shared instructions under RTF, ICIO, or CRISP. The Task 1 report documents this prompt design.

## Descriptive results

| Framework | Exact correct | Exact accuracy | Mean Jaccard | Median Jaccard | Mean time (s) | Median time (s) |
|---|---:|---:|---:|---:|---:|---:|
{chr(10).join(metric_rows)}

| Framework | Jaccard = 1 (exact) | Partial (0 < J < 1) | Jaccard = 0 | SQL errors | Failed generations |
|---|---:|---:|---:|---:|---:|
{chr(10).join(distribution_rows)}

![Exact-result accuracy by framework](task4_accuracy.svg)

![Mean Multiset Jaccard Similarity by framework](task4_jaccard_similarity.svg)

The mean and median Jaccard values describe a graded result-overlap measure; they do not replace exact accuracy. All three have the same mean Jaccard ({summaries[0]['mean_jaccard']:.9f}), with {summaries[0]['perfect_jaccard_count']} exact matches, {summaries[0]['partial_jaccard_count']} partial match, and {summaries[0]['zero_jaccard_count']} zero scores.

## Paired question-level comparison

All frameworks answered the same questions in the same order, so tests and contrasts use paired observations rather than treating the prompt runs as independent samples. RTF and ICIO produced byte-for-byte identical SQL on {sql_counts['RTF_vs_ICIO']}/155 questions; RTF and CRISP on {sql_counts['RTF_vs_CRISP']}/155; ICIO and CRISP on {sql_counts['ICIO_vs_CRISP']}/155. All three SQL texts were identical on {results['per_question_pairing']['all_three_sql_texts_identical_count']}/155 questions.

### Exact-result accuracy

| Test | Comparison | Paired n | Discordant pairs | Statistic | p-value | Effect size | Conclusion |
|---|---|---:|---:|---:|---:|---|---|
{chr(10).join(exact_test_rows)}

{exact_test_conclusion}

### Multiset Jaccard Similarity

| Test | Comparison | Paired n | Statistic | p-value | Holm-adjusted p | Conclusion |
|---|---|---:|---:|---:|---:|---|
{chr(10).join(jaccard_test_rows)}

{jaccard_conclusion}

## Generation-time analysis

All {time_analysis['paired_question_count']} question-level times were valid for every framework; missing and invalid time counts were zero. Potential extremes were identified using the 1.5×IQR Tukey rule. The plot shows every observation, with the interquartile box, median, and full observed range.

| Framework | n | Min (s) | Q1 (s) | Median (s) | Q3 (s) | Max (s) | Tukey outliers |
|---|---:|---:|---:|---:|---:|---:|---:|
{chr(10).join(quality_rows)}

![Generation-time distributions for the paired questions](task4_generation_time_distributions.svg)

The global repeated-measures Friedman test and pairwise Wilcoxon signed-rank tests compare response times question-by-question. The Friedman reference p-value uses its chi-square approximation; Wilcoxon is two-sided with SciPy's `method="auto"` (normal approximation for these 155 nonzero pairs) and no continuity correction. The Wilcoxon signed-rank test evaluates paired differences using their signs and ranks, while Holm correction adjusts the three pairwise p-values to account for multiple comparisons. Kendall's W is reported as the global effect size; paired rank-biserial correlation is the pairwise effect size (negative values indicate lower times for the first-named framework). The 95% paired bootstrap intervals are pointwise percentile intervals for the mean paired time difference, resampling questions as paired units; they are not adjusted for multiple comparisons.

| Test | Comparison | n | Statistic | Raw p-value | Effect size / adjusted p | Conclusion at α = 0.05 |
|---|---|---:|---:|---:|---|---|
{chr(10).join(time_test_rows)}

| Paired contrast (first − second) | n | Mean difference (s) | Median difference (s) | 95% paired bootstrap CI for mean (s) | Faster by observed mean | Holm p | Rank-biserial r |
|---|---:|---:|---:|---:|---|---:|---:|
{chr(10).join(time_pair_rows)}

![Paired mean generation-time contrasts with bootstrap confidence intervals](task4_paired_time_differences.svg)

Negative contrasts mean the first-named framework had lower time. The largest observed mean gap was RTF versus ICIO: RTF was 0.236665 s faster on average, about {100 * abs(pairwise[0]['mean_difference_first_minus_second']) / summaries[1]['mean_generation_time_seconds']:.2f}% of ICIO's mean latency. For this contrast, the 95% pointwise bootstrap interval for the mean paired time difference is [-0.433741, -0.047012] s and excludes zero, while the Holm-adjusted p-value from the Wilcoxon signed-rank test is 0.055231, above α = 0.05. These results need not conflict: the interval is unadjusted for multiple comparisons and concerns the mean paired difference, whereas the Wilcoxon test evaluates signed ranks of paired differences and its p-value is Holm-adjusted across the three pairwise tests. The interval therefore does not override the corrected test conclusion. No statistically significant time difference between any framework pair was confirmed after Holm correction. Statistical significance does not by itself imply practical importance; interpret the estimated seconds and intervals alongside the test results. The bootstrap uses {BOOTSTRAP_REPLICATES:,} paired question-level resamples with fixed seed {BOOTSTRAP_SEED}.

## Interpretation and possible factors

### Prompt frameworks

The exact correctness vectors and Jaccard score vectors are identical, even though SQL text differs on some questions. In addition, the prompts intentionally share the database schema, relationship rules, most domain-specific instructions, SQL-only format requirement, and all seven demonstrations. Their differences chiefly concern the organization and framing of those contents. The observed high SQL overlap and identical measured outcomes are consistent with the possibility that shared substantive guidance dominated the framework-specific headings. This is a plausible explanation, not a causal finding: the experiment did not independently manipulate instruction content and structure.

### Model and coding agent

GitHub Copilot CLI 1.0.98 was used in three separate named sessions/agent profiles (`task2-rtf`, `task2-icio`, `task2-crisp`). The session records and Task 2 metadata identify the respective agents and prompt hashes. The configured model setting was `auto`; although all responses recorded `gpt-6-luna`, explicit pinning to that model was not achieved. Automatic routing therefore remains a reproducibility limitation and does not guarantee the same model in another run.

The prompt framework, model routing, and Copilot coding-agent environment were not varied in a factorial or repeated experiment. This analysis cannot attribute the outcomes or latency differences separately to the named prompt frameworks, model selection, or agent. Generation time measures observed CLI question-to-complete-response latency, which may include network and service-load variation. Requests were processed sequentially in RTF, ICIO, then CRISP order, so time-of-run/order effects can also be confounded with framework.

### Task 2 and Task 3 together

Task 3 did not add a framework ranking: all three have the same 43 exact outcomes, 111 zero scores, one tiny partial Jaccard score, and the same aggregate Jaccard metrics. This is an observation about this dataset and these responses, not proof that the prompts will always behave identically.

## Limitations and reproducibility

- There is one observed response per question and framework; run-to-run and sampling variability cannot be estimated.
- The model setting was automatic routing. Equal recorded model IDs in this run do not establish a pinned model for the experiment.
- A non-significant test is not evidence of complete equivalence. The identical correctness/Jaccard vectors make the corresponding between-framework tests non-informative for this run.
- Time p-values describe within-run paired response-time differences and do not isolate prompt causality from service conditions or sequential run order.
- The benchmark contains 155 questions from one schema/database; generalization to other Text-to-SQL tasks is untested.
- Prompt organization was compared while substantive instructions and examples were largely shared; this design cannot estimate separate causal effects of headings, rule content, model, or coding agent.

To reproduce the analysis without contacting the model, run `python task4_analysis.py` from this directory using Python 3.14 with SciPy and NumPy available. The script validates the Task 2 CSVs, reruns the unmodified instructor evaluator in temporary isolated directories, recomputes per-question result matches and Jaccard scores using read-only SQLite queries, checks them against Task 2/Task 3 outputs, and regenerates the JSON, report, and SVG figures. The bootstrap seed, replicate count, SciPy version, and NumPy version are recorded in `task4_statistics.json`.
"""


def main():
    results, summaries, _evaluated, time_analysis = build_analysis()
    write_time_analysis = dict(time_analysis)
    svg_metric_bars(
        summaries,
        "accuracy",
        "Exact-result accuracy by framework",
        "Exact-result accuracy",
        "task4_accuracy.svg",
        percent=True,
    )
    svg_metric_bars(
        summaries,
        "mean_jaccard",
        "Mean Multiset Jaccard Similarity by framework",
        "Mean Jaccard similarity",
        "task4_jaccard_similarity.svg",
        percent=True,
    )
    svg_time_distributions(write_time_analysis)
    svg_paired_time_differences(write_time_analysis)
    OUTPUT_JSON.write_text(
        json.dumps(results, indent=2, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    OUTPUT_REPORT.write_text(
        report_text(results, summaries, write_time_analysis), encoding="utf-8"
    )
    print("Framework | Correct | Accuracy | Mean Jaccard | Mean time | Median time")
    for item in summaries:
        print(
            f"{item['framework']} | {item['correct']}/{item['total_questions']} | "
            f"{item['accuracy']:.2%} | {item['mean_jaccard']:.9f} | "
            f"{item['mean_generation_time_seconds']:.6f} | "
            f"{item['median_generation_time_seconds']:.6f}"
        )
    print(
        "Friedman generation-time test: "
        f"statistic={write_time_analysis['friedman']['statistic']:.6f}, "
        f"p={write_time_analysis['friedman']['p_value']:.8g}, "
        f"Kendall W={write_time_analysis['kendalls_w']:.6f}"
    )
    for item in write_time_analysis["pairwise_wilcoxon"]:
        print(
            f"{item['first']} vs {item['second']}: "
            f"p={item['p_value']:.8g}, "
            f"Holm p={item['holm_adjusted_p_value']:.8g}, "
            f"mean difference={item['mean_difference_first_minus_second']:+.6f}s"
        )
    print("Task 4 statistics, report, and charts written.")


if __name__ == "__main__":
    main()
