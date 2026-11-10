"""Split source and relevant text files into AST-aware or line-based JSONL chunks."""

from __future__ import annotations

import argparse
import ast
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


TOKEN_PATTERN = re.compile(r"\w+|[^\w\s]", re.UNICODE)
EXCLUDED_DIRECTORIES = {
    ".git",
    ".venv",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "__pycache__",
    "build",
    "coverage",
    "dist",
    "env",
    "generated",
    "gen",
    "htmlcov",
    "node_modules",
    "site-packages",
    "vendor",
    "venv",
}
TEXT_EXTENSIONS = {
    ".adoc",
    ".cfg",
    ".conf",
    ".css",
    ".csv",
    ".html",
    ".ini",
    ".json",
    ".md",
    ".markdown",
    ".properties",
    ".rst",
    ".toml",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}
TEXT_FILENAMES = {
    ".gitignore",
    "dockerfile",
    "license",
    "makefile",
    "readme",
}
EXCLUDED_FILENAMES = {
    "package-lock.json",
    "pnpm-lock.yaml",
    "poetry.lock",
    "yarn.lock",
}
ENV_TEMPLATE_FILENAMES = {
    ".env.example",
    ".env.sample",
    ".env.template",
}


@dataclass(frozen=True)
class SourceUnit:
    start_line: int
    end_line: int
    symbol: str
    text: str


def estimate_tokens(text: str) -> int:
    """Estimate tokens by counting word and punctuation groups."""
    return len(TOKEN_PATTERN.findall(text))


def node_start_line(node: ast.AST) -> int:
    """Include decorators in the source range for decorated definitions."""
    decorators = getattr(node, "decorator_list", ())
    if decorators:
        return min(decorator.lineno for decorator in decorators)
    return node.lineno


def line_text(lines: list[str], start: int, end: int) -> str:
    return "".join(lines[start - 1 : end])


def read_utf8_text(path: Path) -> str | None:
    raw = path.read_bytes()
    if b"\0" in raw:
        return None
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return None


def class_units(
    node: ast.ClassDef, lines: list[str], target_tokens: int
) -> list[SourceUnit]:
    start = node_start_line(node)
    end = node.end_lineno or node.lineno
    whole_text = line_text(lines, start, end)
    if estimate_tokens(whole_text) <= target_tokens:
        return [SourceUnit(start, end, node.name, whole_text)]

    units: list[SourceUnit] = []
    cursor = start
    for member in node.body:
        member_start = node_start_line(member)
        member_end = member.end_lineno or member.lineno
        if cursor < member_start:
            label = f"{node.name} (class header)" if cursor == start else node.name
            units.append(
                SourceUnit(
                    cursor,
                    member_start - 1,
                    label,
                    line_text(lines, cursor, member_start - 1),
                )
            )
        member_name = getattr(member, "name", type(member).__name__)
        units.append(
            SourceUnit(
                member_start,
                member_end,
                f"{node.name}.{member_name}",
                line_text(lines, member_start, member_end),
            )
        )
        cursor = member_end + 1

    if cursor <= end:
        units.append(
            SourceUnit(cursor, end, node.name, line_text(lines, cursor, end))
        )
    return units


def split_long_line(line: str, max_tokens: int) -> list[str]:
    """Split an unusually long physical line while preserving every character."""
    pieces: list[str] = []
    remaining = line
    while estimate_tokens(remaining) > max_tokens:
        low, high = 1, len(remaining)
        while low < high:
            middle = (low + high + 1) // 2
            if estimate_tokens(remaining[:middle]) <= max_tokens:
                low = middle
            else:
                high = middle - 1
        cut = low
        whitespace = remaining.rfind(" ", 0, cut + 1)
        if whitespace > cut // 2:
            cut = whitespace + 1
        pieces.append(remaining[:cut])
        remaining = remaining[cut:]
    if remaining:
        pieces.append(remaining)
    return pieces


def split_oversized_unit(unit: SourceUnit, max_tokens: int) -> list[SourceUnit]:
    if estimate_tokens(unit.text) <= max_tokens:
        return [unit]

    result: list[SourceUnit] = []
    pending = ""
    pending_start = unit.start_line
    pending_end = unit.start_line
    current_line = unit.start_line
    for line in unit.text.splitlines(keepends=True):
        pieces = split_long_line(line, max_tokens)
        for piece in pieces:
            if pending and estimate_tokens(pending + piece) > max_tokens:
                result.append(
                    SourceUnit(
                        pending_start,
                        pending_end,
                        unit.symbol,
                        pending,
                    )
                )
                pending = ""
                pending_start = current_line
            pending += piece
            pending_end = current_line
        current_line += 1

    if pending:
        result.append(
            SourceUnit(pending_start, pending_end, unit.symbol, pending)
        )
    return result


def source_units(
    tree: ast.Module,
    lines: list[str],
    target_tokens: int,
    max_tokens: int,
) -> list[SourceUnit]:
    units: list[SourceUnit] = []
    cursor = 1
    for node in tree.body:
        start = node_start_line(node)
        end = node.end_lineno or node.lineno
        if cursor < start:
            units.append(
                SourceUnit(
                    cursor,
                    start - 1,
                    "module",
                    line_text(lines, cursor, start - 1),
                )
            )

        if isinstance(node, ast.ClassDef):
            units.extend(class_units(node, lines, target_tokens))
        else:
            units.append(
                SourceUnit(
                    start,
                    end,
                    getattr(node, "name", "module"),
                    line_text(lines, start, end),
                )
            )
        cursor = end + 1

    if cursor <= len(lines):
        units.append(
            SourceUnit(
                cursor,
                len(lines),
                "module",
                line_text(lines, cursor, len(lines)),
            )
        )

    split_units: list[SourceUnit] = []
    for unit in units:
        split_units.extend(split_oversized_unit(unit, max_tokens))
    return split_units


def chunk_file(
    path: Path, repo_root: Path, target_tokens: int, max_tokens: int
) -> list[dict[str, object]]:
    source = read_utf8_text(path)
    if source is None:
        return []
    lines = source.splitlines(keepends=True)
    if not lines:
        return []
    tree = ast.parse(source, filename=str(path))
    units = source_units(tree, lines, target_tokens, max_tokens)

    chunks: list[dict[str, object]] = []
    current: list[SourceUnit] = []
    current_tokens = 0

    def flush() -> None:
        nonlocal current, current_tokens
        if not current:
            return
        text = "".join(unit.text for unit in current)
        symbols = list(dict.fromkeys(unit.symbol for unit in current))
        chunks.append(
            {
                "file": path.relative_to(repo_root).as_posix(),
                "chunk_index": len(chunks),
                "start_line": current[0].start_line,
                "end_line": current[-1].end_line,
                "symbols": symbols,
                "estimated_tokens": estimate_tokens(text),
                "text": text,
            }
        )
        current = []
        current_tokens = 0

    for unit in units:
        unit_tokens = estimate_tokens(unit.text)
        if current and current_tokens + unit_tokens > target_tokens:
            flush()
        current.append(unit)
        current_tokens += unit_tokens
    flush()
    return chunks


def chunk_text_file(
    path: Path, repo_root: Path, target_tokens: int, max_tokens: int
) -> list[dict[str, object]]:
    source = read_utf8_text(path)
    if source is None:
        return []

    chunks: list[dict[str, object]] = []
    current_text = ""
    current_tokens = 0
    start_line = 0

    def flush(end_line: int) -> None:
        nonlocal current_text, current_tokens, start_line
        if not current_text:
            return
        chunks.append(
            {
                "file": path.relative_to(repo_root).as_posix(),
                "chunk_index": len(chunks),
                "start_line": start_line,
                "end_line": end_line,
                "symbols": ["document"],
                "estimated_tokens": estimate_tokens(current_text),
                "text": current_text,
            }
        )
        current_text = ""
        current_tokens = 0
        start_line = 0

    for line_number, line in enumerate(source.splitlines(keepends=True), start=1):
        for piece in split_long_line(line, max_tokens):
            piece_tokens = estimate_tokens(piece)
            if current_text and current_tokens + piece_tokens > target_tokens:
                flush(line_number - 1 if start_line < line_number else line_number)
            if not current_text:
                start_line = line_number
            current_text += piece
            current_tokens += piece_tokens
    flush(len(source.splitlines()))
    return chunks


def is_excluded(path: Path) -> bool:
    return any(part.lower() in EXCLUDED_DIRECTORIES for part in path.parts)


def is_relevant_file(path: Path) -> bool:
    name = path.name.lower()
    if is_excluded(path) or name in EXCLUDED_FILENAMES:
        return False
    if (
        ".generated." in name
        or ".min." in name
        or name.endswith(("_generated.py", "_autogen.py", "_pb2.py", "_pb2_grpc.py"))
    ):
        return False
    if path.suffix.lower() == ".py" or path.suffix.lower() in TEXT_EXTENSIONS:
        return True
    return name in TEXT_FILENAMES or name in ENV_TEMPLATE_FILENAMES


def is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def build_chunks(
    repo_root: Path, target_tokens: int, max_tokens: int
) -> list[dict[str, object]]:
    if not repo_root.is_dir():
        raise FileNotFoundError(f"Repository directory does not exist: {repo_root}")

    source_files = sorted(
        path
        for path in repo_root.rglob("*")
        if path.is_file() and is_relevant_file(path.relative_to(repo_root))
    )
    chunks: list[dict[str, object]] = []
    for path in source_files:
        if path.suffix.lower() == ".py":
            chunks.extend(chunk_file(path, repo_root, target_tokens, max_tokens))
        else:
            chunks.extend(chunk_text_file(path, repo_root, target_tokens, max_tokens))
    return chunks


def write_jsonl(chunks: Iterable[dict[str, object]], output_path: Path) -> int:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with output_path.open("w", encoding="utf-8", newline="\n") as output:
        for chunk in chunks:
            output.write(json.dumps(chunk, ensure_ascii=False) + "\n")
            count += 1
    return count


def parse_args() -> argparse.Namespace:
    workspace_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser(
        description="Create JSONL chunks from a source repository."
    )
    parser.add_argument(
        "--repo",
        type=Path,
        default=workspace_root / "AI4SE_Playground",
        help="Repository directory to read (default: workspace AI4SE_Playground).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent / "repository_chunks.jsonl",
        help="JSONL output path (default: this script's directory).",
    )
    parser.add_argument("--target-tokens", type=int, default=550)
    parser.add_argument("--max-tokens", type=int, default=700)
    args = parser.parse_args()
    if args.target_tokens <= 0 or args.max_tokens < args.target_tokens:
        parser.error("--target-tokens must be positive and --max-tokens >= target")
    args.repo = args.repo.resolve()
    args.output = args.output.resolve()
    if is_within(args.output, args.repo):
        parser.error("Output must be outside the cloned repository.")
    return args


def main() -> None:
    args = parse_args()
    chunks = build_chunks(args.repo, args.target_tokens, args.max_tokens)
    if not chunks:
        raise ValueError(f"No supported text files found in {args.repo}")
    count = write_jsonl(chunks, args.output)
    print(
        f"Wrote {count} chunks from "
        f"{len({item['file'] for item in chunks})} files to {args.output}"
    )


if __name__ == "__main__":
    main()
