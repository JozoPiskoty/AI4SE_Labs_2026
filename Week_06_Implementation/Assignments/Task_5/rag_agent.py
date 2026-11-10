"""RAG agent: fills the missing methods listed in missing_code.json.

For every task the agent retrieves the top-5 repository chunks (Task 4), asks an
OpenAI model for the method source, replaces that method in the target file and
finally runs the repository's unit tests.
"""
from __future__ import annotations

import argparse
import ast
import getpass
import json
import re
import shutil
import subprocess
import sys
import textwrap
from datetime import datetime
from pathlib import Path

import openai
from openai import OpenAI

ASSIGNMENTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ASSIGNMENTS / "Task_4"))
import match_chunks  # noqa: E402

REPO_ROOT = ASSIGNMENTS.parents[1] / "AI4SE_Playground"
TEST_DIR = REPO_ROOT / "playground"
TASKS_FILE = ASSIGNMENTS / "missing_code.json"
BACKUP_DIR = Path(__file__).resolve().parent / "original_files"
REPORT_FILE = Path(__file__).resolve().parent / "TASK5_RUN_RESULTS.md"

ALLOWED_MODELS = [
    "gpt-6-luna", "gpt-5.6-luna", "gpt-5.4-nano", "gpt-5-nano",
    "gpt-5-mini", "gpt-4.1-nano", "gpt-4o-mini",
]
DEFAULT_MODEL = "gpt-5-mini"
TOP_N = 5
MAX_ATTEMPTS = 2

SYSTEM_PROMPT = (
    "You are a precise Python developer completing a missing method in an existing "
    "code base. Use the provided repository chunks as context. Reply with ONLY the "
    "complete method definition (decorators, signature, docstring and body), as "
    "plain Python without markdown fences or explanations."
)


def log(message: str) -> None:
    print(message, flush=True)


def connect(model: str) -> OpenAI:
    """Ask for the key securely, create the client and test the model."""
    api_key = getpass.getpass("Enter your OpenAI API key (input hidden): ").strip()
    if not api_key:
        sys.exit("No API key entered. Nothing was changed.")
    client = OpenAI(api_key=api_key)
    log(f"Testing API connection with model '{model}'...")
    try:
        client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Reply with the word OK."}],
            max_completion_tokens=200,
        )
    except openai.AuthenticationError as exc:
        sys.exit(f"Authentication failed: {exc.message}\nNo source files were modified.")
    except (openai.PermissionDeniedError, openai.NotFoundError) as exc:
        sys.exit(f"Model '{model}' is not accessible with this key: {exc.message}\n"
                 "No source files were modified.")
    except openai.OpenAIError as exc:
        sys.exit(f"API connection test failed ({type(exc).__name__}): {exc}\n"
                 "No source files were modified.")
    log("API connection OK.")
    return client


def find_method(source: str, class_name: str, method: str) -> ast.FunctionDef:
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and item.name == method:
                    return item
    raise LookupError(f"{class_name}.{method} not found")


def method_span(node: ast.FunctionDef) -> tuple[int, int]:
    """1-based inclusive line range, including decorators."""
    first = min([node.lineno] + [d.lineno for d in node.decorator_list])
    return first, node.end_lineno


def build_prompt(task: dict, chunks: list[dict], current: str) -> str:
    parts = [
        f"Task: implement `{task['class']}.{task['method']}` in `{task['file']}`.",
        f"Docstring / requirement:\n{textwrap.dedent(task['docstring'])}",
        f"Current stub (to be replaced):\n{current}",
        "Relevant repository chunks:",
    ]
    for c in chunks:
        parts.append(
            f"--- {c['file']} lines {c['start_line']}-{c['end_line']} "
            f"(similarity {c['similarity']:.3f}) ---\n{c['text']}"
        )
    parts.append(
        "Return only the full method definition for the target, keeping its name, "
        "signature, decorators and docstring."
    )
    return "\n\n".join(parts)


def clean_response(text: str) -> str:
    text = text.strip()
    fenced = re.search(r"```(?:python)?\n(.*?)```", text, re.S)
    return (fenced.group(1) if fenced else text).strip("\n")


def validate(code: str, method: str) -> str:
    """Return dedented code if it is exactly one function with the right name."""
    code = textwrap.dedent(code)
    tree = ast.parse(code)
    if len(tree.body) != 1 or not isinstance(tree.body[0], (ast.FunctionDef, ast.AsyncFunctionDef)):
        raise ValueError("response is not a single method definition")
    if tree.body[0].name != method:
        raise ValueError(f"method name is {tree.body[0].name!r}, expected {method!r}")
    return code


def solve_task(client: OpenAI, model: str, task: dict) -> str:
    """Retrieve context, query the LLM and write the method into the target file."""
    path = REPO_ROOT / task["file"]
    source = path.read_text(encoding="utf-8")
    node = find_method(source, task["class"], task["method"])
    start, end = method_span(node)
    lines = source.splitlines(keepends=True)
    current = textwrap.dedent("".join(lines[start - 1:end]))
    indent = " " * node.col_offset

    description = (f"Implement {task['class']}.{task['method']} in {task['file']}: "
                   f"{textwrap.dedent(task['docstring']).strip()}")
    log("  - Retrieving top-5 chunks...")
    chunks = match_chunks.retrieve_top_n(embed(description), TOP_N)
    for c in chunks:
        log(f"      #{c['rank']} {c['file']}:{c['start_line']}-{c['end_line']} "
            f"(similarity {c['similarity']:.3f})")
    prompt = build_prompt(task, chunks, current)

    error = ""
    for attempt in range(1, MAX_ATTEMPTS + 1):
        log(f"  - Calling {model} (attempt {attempt}/{MAX_ATTEMPTS})...")
        content = prompt if not error else f"{prompt}\n\nYour previous answer was rejected: {error}"
        try:
            reply = client.chat.completions.create(
                model=model,
                messages=[{"role": "system", "content": SYSTEM_PROMPT},
                          {"role": "user", "content": content}],
            )
            code = validate(clean_response(reply.choices[0].message.content or ""), task["method"])
        except openai.OpenAIError as exc:
            error = f"API error: {exc}"
            log(f"    API error: {exc}")
            continue
        except (SyntaxError, ValueError) as exc:
            error = str(exc)
            log(f"    Invalid response: {error}")
            continue
        new_lines = [(indent + l if l.strip() else l) for l in code.splitlines(keepends=True)]
        if not new_lines[-1].endswith("\n"):
            new_lines[-1] += "\n"
        updated = "".join(lines[:start - 1] + new_lines + lines[end:])
        compile(updated, str(path), "exec")
        path.write_text(updated, encoding="utf-8", newline="")
        log(f"  - Wrote {task['class']}.{task['method']} to {task['file']} "
            f"(lines {start}-{end} replaced)")
        return "success"
    return f"failed: {error}"


_model = None


def embed(text: str):
    """Load the embedding model once and reuse it for every task."""
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        log("Loading embedding model (once)...")
        _model = SentenceTransformer(match_chunks.MODEL_NAME)
    return _model.encode(text, convert_to_numpy=True, normalize_embeddings=True)


def backup_originals(tasks: list[dict]) -> None:
    for file in sorted({t["file"] for t in tasks}):
        target = BACKUP_DIR / file
        if not target.exists():  # keep the very first (stub) version
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(REPO_ROOT / file, target)
    log(f"Original files backed up in {BACKUP_DIR}")


def restore_originals() -> None:
    for backup in BACKUP_DIR.rglob("*.py"):
        shutil.copy2(backup, REPO_ROOT / backup.relative_to(BACKUP_DIR))
        log(f"Restored {backup.relative_to(BACKUP_DIR)}")


def run_tests() -> tuple[int, str]:
    log("Running unit tests (python -m unittest discover -s tests -v)...")
    proc = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        cwd=TEST_DIR, capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    output = proc.stdout + proc.stderr
    log(output.strip().splitlines()[-1] if output.strip() else "(no output)")
    return proc.returncode, output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default=DEFAULT_MODEL, choices=ALLOWED_MODELS)
    parser.add_argument("--restore", action="store_true",
                        help="restore the original stub files and exit")
    args = parser.parse_args()

    if args.restore:
        restore_originals()
        return

    tasks = json.loads(TASKS_FILE.read_text(encoding="utf-8"))
    client = connect(args.model)  # exits before any file is touched on failure
    backup_originals(tasks)

    results = []
    for i, task in enumerate(tasks, start=1):
        log(f"\n[{i}/{len(tasks)}] {task['class']}.{task['method']} ({task['file']})")
        try:
            status = solve_task(client, args.model, task)
        except Exception as exc:  # keep going with the remaining tasks
            status = f"failed: {type(exc).__name__}: {exc}"
        log(f"  => {status}")
        results.append((task, status))

    code, output = run_tests()
    solved = sum(s == "success" for _, s in results)
    lines = [
        "# Task 5 run results", "",
        f"- Date: {datetime.now():%Y-%m-%d %H:%M}",
        f"- Model: {args.model}",
        f"- Methods written: {solved}/{len(results)}", "",
        "| # | Method | Status |", "|---|--------|--------|",
    ]
    lines += [f"| {i} | `{t['class']}.{t['method']}` | {s} |" for i, (t, s) in enumerate(results, 1)]
    lines += ["", f"Unit tests exit code: {code}", "", "```text", output.strip(), "```", ""]
    REPORT_FILE.write_text("\n".join(lines), encoding="utf-8")
    log(f"\nDone: {solved}/{len(results)} methods written; tests exit code {code}.")
    log(f"Results saved to {REPORT_FILE}")


if __name__ == "__main__":
    main()
