from __future__ import annotations

from email import policy
from email.parser import BytesParser
from pathlib import Path
from typing import Any


SUPPORTED_SUFFIXES = {".txt", ".eml"}


def _read_text(path: Path) -> str:
    if path.suffix.lower() == ".eml":
        message = BytesParser(policy=policy.default).parsebytes(path.read_bytes())
        body = message.get_body(preferencelist=("plain",))
        body_text = body.get_content() if body is not None else ""
        headers = [
            f"{key}: {message.get(key)}"
            for key in ("From", "To", "Cc", "Subject", "Date")
            if message.get(key)
        ]
        return "\n".join(headers + ["", str(body_text)]).strip()
    return path.read_text(encoding="utf-8-sig")


def load_corpus(input_dir: Path, output_dir: Path | None = None) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    root = input_dir.expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise ValueError(f"Input directory does not exist or is not a directory: {root}")

    excluded_output = output_dir.expanduser().resolve() if output_dir else None
    documents: list[dict[str, Any]] = []
    issues: list[dict[str, str]] = []
    seen: set[Path] = set()

    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        resolved = path.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        if excluded_output and (resolved == excluded_output or excluded_output in resolved.parents):
            continue
        if path.suffix.lower() not in SUPPORTED_SUFFIXES:
            if path.name not in {".DS_Store", "Thumbs.db"}:
                issues.append({"document": path.relative_to(root).as_posix(), "issue": "Unsupported file type; skipped."})
            continue

        name = path.relative_to(root).as_posix()
        try:
            text = _read_text(path).strip()
            if not text:
                issues.append({"document": name, "issue": "File is empty; no text was processed."})
                documents.append({"id": name, "name": name, "text": "", "status": "empty"})
                continue
            documents.append({"id": name, "name": name, "text": text, "status": "loaded"})
        except (OSError, UnicodeError, ValueError) as exc:
            issues.append({"document": name, "issue": f"Could not read file ({type(exc).__name__}): {exc}"})
            documents.append({"id": name, "name": name, "text": "", "status": "error"})

    if not documents:
        raise ValueError(f"No supported .txt or .eml documents were found in {root}")
    return documents, issues


def batch_documents(documents: list[dict[str, Any]], max_chars: int = 30000) -> list[list[dict[str, Any]]]:
    batches: list[list[dict[str, Any]]] = []
    current: list[dict[str, Any]] = []
    chars = 0
    for document in documents:
        if document["status"] != "loaded":
            continue
        segments: list[str] = []
        segment = ""
        for line in document["text"].splitlines(keepends=True):
            while len(line) > max_chars:
                if segment:
                    segments.append(segment)
                    segment = ""
                segments.append(line[:max_chars])
                line = line[max_chars:]
            if segment and len(segment) + len(line) > max_chars:
                segments.append(segment)
                segment = ""
            segment += line
        if segment:
            segments.append(segment)
        for segment_text in segments or [""]:
            part = {**document, "text": segment_text}
            size = len(segment_text)
            if current and chars + size > max_chars:
                batches.append(current)
                current, chars = [], 0
            current.append(part)
            chars += size
    if current:
        batches.append(current)
    return batches
