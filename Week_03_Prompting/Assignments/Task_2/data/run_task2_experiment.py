"""Run the Task 2 benchmark in three isolated GitHub Copilot CLI sessions."""

import csv
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path


TASK_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = TASK_DIR / "data"
TASK1_DIR = TASK_DIR.parent / "Task_1"
DATASET_PATH = DATA_DIR / "restaurants_dataset.csv"
METADATA_PATH = DATA_DIR / "task2_experiment_metadata.json"
MODEL_SETTING = os.environ.get("TASK2_MODEL_ID", "").strip()
AUTO_MODEL_ROUTING = MODEL_SETTING.lower() == "auto"
EXPECTED_QUESTIONS = 155
TIMEOUT_SECONDS = 180

FRAMEWORKS = {
    "RTF": ("prompt_rtf.txt", "task2-rtf"),
    "ICIO": ("prompt_icio.txt", "task2-icio"),
    "CRISP": ("prompt_crisp.txt", "task2-crisp"),
}
CSV_FIELDS = [
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
]


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def get_cli_path():
    cli = shutil.which("copilot.cmd") or shutil.which("copilot")
    if cli:
        return cli

    appdata = os.environ.get("APPDATA")
    if appdata:
        candidate = Path(appdata) / "npm" / "copilot.cmd"
        if candidate.is_file():
            return str(candidate)
    raise FileNotFoundError(
        "GitHub Copilot CLI was not found. Install it and complete `copilot login`."
    )


def read_questions():
    csv.field_size_limit(1_000_000_000)
    with DATASET_PATH.open(encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        if reader.fieldnames is None or not {"question", "result"}.issubset(
            reader.fieldnames
        ):
            raise ValueError(f"Unexpected dataset columns in {DATASET_PATH}")
        questions = [row["question"] for row in reader]

    if len(questions) != EXPECTED_QUESTIONS:
        raise ValueError(
            f"Expected {EXPECTED_QUESTIONS} benchmark questions, found {len(questions)}"
        )
    return questions


def load_or_create_metadata(prompt_hashes):
    if METADATA_PATH.exists():
        metadata = json.loads(METADATA_PATH.read_text(encoding="utf-8"))
        if metadata.get("model_setting") != MODEL_SETTING:
            raise ValueError(
                "Saved experiment metadata uses a different model setting. "
                "Start a fresh experiment with a new metadata file."
            )
        if metadata.get("prompt_sha256") != prompt_hashes:
            raise ValueError(
                "Task 1 prompts changed since this experiment began. "
                "Do not resume with different prompts."
            )
        return metadata

    metadata = {
        "experiment_started_utc": utc_now(),
        "copilot_cli_version": None,
        "model_setting": MODEL_SETTING,
        "model_selection_note": (
            "The user explicitly approved Copilot Auto routing after the "
            "authenticated model catalog exposed only `auto`. The exact model "
            "ID is recorded for every completed response and may vary."
            if AUTO_MODEL_ROUTING
            else (
                "The exact requested model ID is validated against the model "
                "reported in every completed response."
            )
        ),
        "prompt_sha256": prompt_hashes,
        "sessions": {
            framework: {
                "session_id": str(uuid.uuid4()),
                "agent_name": agent_name,
                "actual_model_ids": [],
                "completed_rows": 0,
            }
            for framework, (_prompt_file, agent_name) in FRAMEWORKS.items()
        },
    }
    METADATA_PATH.write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return metadata


def save_metadata(metadata):
    metadata["last_updated_utc"] = utc_now()
    METADATA_PATH.write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def csv_path(framework):
    return DATA_DIR / f"task2_predictions_{framework.lower()}.csv"


def read_existing_predictions(framework, questions):
    path = csv_path(framework)
    if not path.exists():
        return []

    with path.open(encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        if reader.fieldnames is None or not set(CSV_FIELDS).issubset(
            reader.fieldnames
        ):
            raise ValueError(f"Unexpected prediction CSV columns in {path}")
        rows = list(reader)

    if len(rows) > len(questions):
        raise ValueError(f"{path} contains more rows than the benchmark.")
    if [row["question"] for row in rows] != questions[: len(rows)]:
        raise ValueError(
            f"{path} does not match the original question order. "
            "Refusing to overwrite or reorder predictions."
        )
    if any(row["framework"] != framework for row in rows):
        raise ValueError(f"{path} contains rows for a different framework.")
    return rows


def create_agent_profile(agent_dir, framework, agent_name, prompt_text):
    placeholder = "[INSERT QUESTION HERE]"
    if prompt_text.count(placeholder) != 1:
        raise ValueError(
            f"Expected exactly one question placeholder in the {framework} prompt."
        )

    instructions = prompt_text.replace(
        placeholder,
        "The natural-language question is supplied as the current user message.",
    )
    profile = (
        "---\n"
        f"name: {agent_name}\n"
        f'description: Apply the final {framework} Text-to-SQL prompt to one question.\n'
        "tools: []\n"
        "---\n"
        f"{instructions}\n"
    )
    agents_dir = agent_dir / ".github" / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)
    (agents_dir / f"{agent_name}.agent.md").write_text(
        profile, encoding="utf-8"
    )


def parse_events(stdout):
    events = []
    for line in stdout.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(event, dict) and isinstance(event.get("type"), str):
            events.append(event)
    return events


def event_time(event):
    timestamp = event.get("timestamp")
    if not timestamp:
        return None
    try:
        return datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError:
        return None


def safe_error(text):
    cleaned = " ".join(text.split())
    for prefix in ("ghp_", "github_pat_", "gho_", "ghu_", "ghs_", "ghr_"):
        while prefix in cleaned:
            start = cleaned.index(prefix)
            end = start + len(prefix)
            while end < len(cleaned) and cleaned[end] not in " \t\r\n\"'":
                end += 1
            cleaned = cleaned[:start] + "[REDACTED]" + cleaned[end:]
    return cleaned[-1000:]


def generate_one(
    cli_path,
    working_dir,
    agent_dir,
    framework,
    agent_name,
    session_id,
    question,
    first_request,
):
    command = [
        cli_path,
        "-C",
        str(working_dir),
        "--session-id",
        session_id,
    ]
    if first_request:
        command.extend(["--name", f"Task 2 {framework}"])
    command.extend(
        [
            "--model",
            MODEL_SETTING,
            "--agent",
            agent_name,
            "--add-dir",
            str(agent_dir),
            "--disable-builtin-mcps",
            "--output-format",
            "json",
            "--stream",
            "off",
            "--prompt",
            question,
        ]
    )

    try:
        completed = subprocess.run(
            command,
            cwd=working_dir,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=TIMEOUT_SECONDS,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        return {
            "predicted_sql": "",
            "model_id": "",
            "generation_time_seconds": "",
            "generation_status": "FAILED",
            "error": f"Timed out after {TIMEOUT_SECONDS} seconds.",
            "request_id": "",
        }
    except OSError as error:
        return {
            "predicted_sql": "",
            "model_id": "",
            "generation_time_seconds": "",
            "generation_status": "FAILED",
            "error": safe_error(str(error)),
            "request_id": "",
        }

    events = parse_events(completed.stdout)
    matching_user_events = [
        event
        for event in events
        if event.get("type") == "user.message"
        and event.get("data", {}).get("content") == question
    ]
    if not matching_user_events:
        error_text = completed.stderr or completed.stdout
        return {
            "predicted_sql": "",
            "model_id": "",
            "generation_time_seconds": "",
            "generation_status": "FAILED",
            "error": safe_error(
                error_text or f"CLI exited with status {completed.returncode}."
            ),
            "request_id": "",
        }

    user_event = matching_user_events[-1]
    user_time = event_time(user_event)
    user_interaction_id = user_event.get("data", {}).get("interactionId")
    later_assistant_events = []
    for event in events:
        if event.get("type") != "assistant.message":
            continue
        data = event.get("data", {})
        if not isinstance(data.get("content"), str):
            continue
        if (
            user_interaction_id
            and data.get("interactionId")
            and data["interactionId"] != user_interaction_id
        ):
            continue
        assistant_time = event_time(event)
        if user_time and assistant_time and assistant_time < user_time:
            continue
        later_assistant_events.append(event)

    if not later_assistant_events:
        error_text = completed.stderr or f"CLI exited with status {completed.returncode}."
        return {
            "predicted_sql": "",
            "model_id": "",
            "generation_time_seconds": "",
            "generation_status": "FAILED",
            "error": safe_error(error_text),
            "request_id": user_event.get("data", {}).get("messageId", ""),
        }

    assistant_event = later_assistant_events[-1]
    content = assistant_event["data"]["content"]
    actual_model_id = assistant_event["data"].get("model", "")
    assistant_time = event_time(assistant_event)
    duration = (
        (assistant_time - user_time).total_seconds()
        if user_time and assistant_time
        else ""
    )
    if duration != "" and duration < 0:
        duration = ""
    duration_text = f"{duration:.6f}" if duration != "" else ""
    if not AUTO_MODEL_ROUTING and actual_model_id != MODEL_SETTING:
        return {
            "predicted_sql": content,
            "model_id": actual_model_id,
            "generation_time_seconds": duration_text,
            "generation_status": "FAILED",
            "error": (
                f"Requested model {MODEL_SETTING!r}, but the response reported "
                f"{actual_model_id!r}."
            ),
            "request_id": assistant_event["data"].get("messageId", ""),
        }
    if not content.strip() or completed.returncode != 0:
        return {
            "predicted_sql": "",
            "model_id": actual_model_id,
            "generation_time_seconds": duration_text,
            "generation_status": "FAILED",
            "error": safe_error(
                completed.stderr or "The model returned an empty answer."
            ),
            "request_id": assistant_event["data"].get("messageId", ""),
        }

    return {
        "predicted_sql": content,
        "model_id": actual_model_id,
        "generation_time_seconds": duration_text,
        "generation_status": "SUCCESS",
        "error": "",
        "request_id": assistant_event["data"].get("messageId", ""),
    }


def main():
    if not MODEL_SETTING:
        raise ValueError(
            "Set TASK2_MODEL_ID to an explicit model setting. Use a concrete "
            "model ID, or `auto` only when automatic routing has been approved."
        )
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    questions = read_questions()
    prompt_texts = {
        framework: (TASK1_DIR / filename).read_text(encoding="utf-8")
        for framework, (filename, _agent_name) in FRAMEWORKS.items()
    }
    prompt_hashes = {
        framework: hashlib.sha256(text.encode("utf-8")).hexdigest()
        for framework, text in prompt_texts.items()
    }
    cli_path = get_cli_path()
    metadata = load_or_create_metadata(prompt_hashes)

    version = subprocess.run(
        [cli_path, "--version"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=30,
        check=False,
    )
    metadata["copilot_cli_version"] = safe_error(
        version.stdout.strip() or version.stderr.strip()
    )
    save_metadata(metadata)

    with tempfile.TemporaryDirectory(prefix="task2-copilot-experiment-") as temp:
        root = Path(temp)
        agent_dir = root / "agents"
        working_dir = root / "working"
        working_dir.mkdir()

        for framework, (_prompt_file, agent_name) in FRAMEWORKS.items():
            create_agent_profile(
                agent_dir, framework, agent_name, prompt_texts[framework]
            )

        for framework, (_prompt_file, agent_name) in FRAMEWORKS.items():
            session = metadata["sessions"][framework]
            rows = read_existing_predictions(framework, questions)
            output_path = csv_path(framework)
            write_header = not output_path.exists()
            with output_path.open(
                "a", encoding="utf-8", newline=""
            ) as destination:
                writer = csv.DictWriter(
                    destination, fieldnames=CSV_FIELDS, extrasaction="ignore"
                )
                if write_header:
                    writer.writeheader()
                    destination.flush()

                for index in range(len(rows), len(questions)):
                    question = questions[index]
                    result = generate_one(
                        cli_path=cli_path,
                        working_dir=working_dir,
                        agent_dir=agent_dir,
                        framework=framework,
                        agent_name=agent_name,
                        session_id=session["session_id"],
                        question=question,
                        first_request=(index == 0 and not rows),
                    )
                    row = {
                        "question": question,
                        **result,
                        "framework": framework,
                        "attempt_count": 1,
                        "session_id": session["session_id"],
                    }
                    writer.writerow(row)
                    destination.flush()
                    rows.append(row)

                    model_id = result["model_id"]
                    if model_id and model_id not in session["actual_model_ids"]:
                        session["actual_model_ids"].append(model_id)
                    session["completed_rows"] = len(rows)
                    save_metadata(metadata)

                    if len(rows) == 1 or len(rows) % 5 == 0:
                        print(
                            f"{framework}: {len(rows)}/{len(questions)} "
                            f"({result['generation_status']})",
                            flush=True,
                        )
                    if index == 0 and result["generation_status"] != "SUCCESS":
                        raise RuntimeError(
                            f"First {framework} request failed; stopping before "
                            f"submitting the remaining questions: {result['error']}"
                        )

            print(
                f"{framework} complete: {len(rows)}/{len(questions)} rows; "
                f"models={session['actual_model_ids']}",
                flush=True,
            )

    metadata["experiment_finished_utc"] = utc_now()
    save_metadata(metadata)
    print("Prediction files and metadata saved.", flush=True)


if __name__ == "__main__":
    main()
