"""Retrieve the chunks most similar to a query embedding."""

from __future__ import annotations

import argparse
import json
import math
import sqlite3
import sys
from contextlib import closing
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

import numpy as np


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIMENSIONS = 384
DEFAULT_TOP_N = 5
NORM_TOLERANCE = 1e-6
DATABASE_PATH = (
    Path(__file__).resolve().parent.parent / "Task_3" / "chunk_embeddings.db"
)


@dataclass(frozen=True)
class ChunkIndex:
    metadata: list[dict[str, Any]]
    embeddings: np.ndarray


_index_cache: dict[Path, ChunkIndex] = {}


def load_index(database_path: Path = DATABASE_PATH) -> ChunkIndex:
    """Load chunks and embeddings from the SQLite database in read-only mode."""
    database_path = Path(database_path).resolve()
    if database_path in _index_cache:
        return _index_cache[database_path]
    if not database_path.is_file():
        raise FileNotFoundError(f"Embedding database not found: {database_path}")

    uri = f"{database_path.as_uri()}?mode=ro"
    with closing(sqlite3.connect(uri, uri=True)) as database:
        rows = database.execute(
            """
            SELECT file, chunk_index, start_line, end_line, symbols, text,
                   model_name, embedding
            FROM chunk_embeddings
            ORDER BY file, chunk_index
            """
        ).fetchall()
    if not rows:
        raise ValueError(f"No embeddings found in {database_path}")

    metadata = []
    vectors = []
    for file, chunk_index, start_line, end_line, symbols, text, model, raw in rows:
        if model != MODEL_NAME:
            raise ValueError(
                f"{file} chunk {chunk_index} uses model {model!r}, expected {MODEL_NAME!r}"
            )
        vector = np.asarray(json.loads(raw), dtype=np.float64)
        if vector.shape != (EMBEDDING_DIMENSIONS,):
            raise ValueError(
                f"{file} chunk {chunk_index} has shape {vector.shape}, "
                f"expected ({EMBEDDING_DIMENSIONS},)"
            )
        if not np.all(np.isfinite(vector)):
            raise ValueError(f"{file} chunk {chunk_index} has non-finite values")
        if abs(np.linalg.norm(vector) - 1.0) > NORM_TOLERANCE:
            raise ValueError(f"{file} chunk {chunk_index} is not unit length")
        vectors.append(vector)
        metadata.append(
            {
                "file": file,
                "chunk_index": chunk_index,
                "start_line": start_line,
                "end_line": end_line,
                "symbols": json.loads(symbols),
                "text": text,
            }
        )

    index = ChunkIndex(metadata, np.vstack(vectors))
    _index_cache[database_path] = index
    return index


def normalize_query(query_embedding: Sequence[float] | np.ndarray) -> np.ndarray:
    query = np.asarray(query_embedding, dtype=np.float64)
    if query.shape != (EMBEDDING_DIMENSIONS,):
        raise ValueError(
            f"Query embedding has shape {query.shape}, expected ({EMBEDDING_DIMENSIONS},)"
        )
    if not np.all(np.isfinite(query)):
        raise ValueError("Query embedding contains non-finite values")
    norm = np.linalg.norm(query)
    if norm == 0:
        raise ValueError("Query embedding must not be a zero vector")
    return query / norm


def retrieve_top_n(
    query_embedding: Sequence[float] | np.ndarray,
    n: int = DEFAULT_TOP_N,
    database_path: Path = DATABASE_PATH,
) -> list[dict[str, Any]]:
    """Return the n chunks with the highest cosine similarity to the query."""
    if isinstance(n, bool) or not isinstance(n, (int, np.integer)):
        raise TypeError("n must be an integer")
    if n < 1:
        raise ValueError("n must be at least 1")

    index = load_index(database_path)
    query = normalize_query(query_embedding)
    scores = index.embeddings @ query

    count = len(scores)
    n = min(int(n), count)
    if n < count:
        candidates = np.argpartition(-scores, n - 1)[:n]
    else:
        candidates = np.arange(count)
    # Tie-break on index so equal scores give a deterministic order.
    ranked = sorted(candidates, key=lambda i: (-scores[i], i))

    return [
        {
            "rank": rank,
            "similarity": float(scores[i]),
            "file": index.metadata[i]["file"],
            "start_line": index.metadata[i]["start_line"],
            "end_line": index.metadata[i]["end_line"],
            "symbols": index.metadata[i]["symbols"],
            "text": index.metadata[i]["text"],
        }
        for rank, i in enumerate(ranked, start=1)
    ]


def embed_query(text: str) -> np.ndarray:
    """Embed query text with the same model used for the stored chunks."""
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer(MODEL_NAME)
    return model.encode(text, convert_to_numpy=True, normalize_embeddings=True)


def positive_int(value: str) -> int:
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("must be at least 1")
    return number


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Find the repository chunks most relevant to a text query."
    )
    parser.add_argument("query", help="Task or question to search for")
    parser.add_argument(
        "-n",
        "--top-n",
        type=positive_int,
        default=DEFAULT_TOP_N,
        help=f"Number of chunks to return (default: {DEFAULT_TOP_N})",
    )
    args = parser.parse_args()
    if not args.query.strip():
        parser.error("query must not be empty")

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    results = retrieve_top_n(embed_query(args.query), args.top_n)
    for result in results:
        symbols = ", ".join(result["symbols"])
        print(
            f"#{result['rank']}  score={result['similarity']:.4f}  "
            f"{result['file']}:{result['start_line']}-{result['end_line']}  "
            f"[{symbols}]"
        )
        print(result["text"].rstrip())
        print("-" * 72)


if __name__ == "__main__":
    main()
