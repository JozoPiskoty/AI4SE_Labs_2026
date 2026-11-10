"""Generate and store embeddings for the Task 2 repository chunks."""

from __future__ import annotations

import json
import math
import sqlite3
from pathlib import Path

import torch
from sentence_transformers import SentenceTransformer


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIMENSIONS = 384
MODEL_INPUT_LIMIT = 256
BATCH_SIZE = 32
TASK_DIR = Path(__file__).resolve().parent
CHUNKS_PATH = TASK_DIR.parent / "Task_2" / "repository_chunks.jsonl"
DATABASE_PATH = TASK_DIR / "chunk_embeddings.db"


def read_chunks(path: Path) -> list[dict]:
    chunks = []
    with path.open(encoding="utf-8") as source:
        for line_number, line in enumerate(source, start=1):
            try:
                chunk = json.loads(line)
                if not isinstance(chunk, dict):
                    raise ValueError("chunk must be a JSON object")
                for key in (
                    "file",
                    "chunk_index",
                    "start_line",
                    "end_line",
                    "symbols",
                    "estimated_tokens",
                    "text",
                ):
                    if key not in chunk:
                        raise ValueError(f"missing field {key!r}")
                if not isinstance(chunk["text"], str):
                    raise ValueError("text must be a string")
                chunks.append(chunk)
            except (json.JSONDecodeError, ValueError) as error:
                raise ValueError(f"{path}, line {line_number}: {error}") from error
    if not chunks:
        raise ValueError(f"No chunks found in {path}")
    return chunks


def embed_chunks(
    chunks: list[dict], model: SentenceTransformer
) -> tuple[list[list[float]], list[int]]:
    tokenizer = model.tokenizer
    limit = min(MODEL_INPUT_LIMIT, model.max_seq_length)
    special_token_count = tokenizer.num_special_tokens_to_add(pair=False)
    if (
        special_token_count != 2
        or tokenizer.cls_token_id is None
        or tokenizer.sep_token_id is None
    ):
        raise ValueError("Expected the model's BERT [CLS]/[SEP] token format")
    window_size = limit - special_token_count
    if window_size <= 0:
        raise ValueError("Model input limit leaves no room for content tokens")
    if model.get_sentence_embedding_dimension() != EMBEDDING_DIMENSIONS:
        raise ValueError(f"Expected {EMBEDDING_DIMENSIONS}-dimensional embeddings")

    windows = []
    owners = []
    counts = [0] * len(chunks)
    for index, chunk in enumerate(chunks):
        token_ids = tokenizer.encode(
            chunk["text"], add_special_tokens=False, truncation=False
        )
        for start in range(0, max(1, len(token_ids)), window_size):
            content_ids = token_ids[start : start + window_size]
            input_ids = [tokenizer.cls_token_id, *content_ids, tokenizer.sep_token_id]
            if len(input_ids) > limit:
                raise ValueError("Token window exceeds the model input limit")
            windows.append(
                {"input_ids": input_ids, "attention_mask": [1] * len(input_ids)}
            )
            owners.append(index)
            counts[index] += 1

    sums = torch.zeros((len(chunks), EMBEDDING_DIMENSIONS), dtype=torch.float64)
    model.eval()
    with torch.inference_mode():
        for start in range(0, len(windows), BATCH_SIZE):
            batch = tokenizer.pad(
                windows[start : start + BATCH_SIZE],
                padding=True,
                return_tensors="pt",
            )
            batch = {key: value.to(model.device) for key, value in batch.items()}
            embeddings = model(batch)["sentence_embedding"].cpu().to(torch.float64)
            if embeddings.shape != (len(batch["input_ids"]), EMBEDDING_DIMENSIONS):
                raise ValueError("Model returned an unexpected embedding shape")
            for owner, embedding in zip(
                owners[start : start + BATCH_SIZE], embeddings
            ):
                sums[owner] += embedding

    vectors = []
    for index, total in enumerate(sums):
        mean = total / counts[index]
        norm = torch.linalg.vector_norm(mean).item()
        if not math.isfinite(norm) or norm == 0:
            raise ValueError(f"Chunk {index} produced an invalid embedding")
        vector = (mean / norm).tolist()
        if not all(math.isfinite(value) for value in vector):
            raise ValueError(f"Chunk {index} produced non-finite values")
        vectors.append(vector)
    return vectors, counts


def save_embeddings(
    path: Path,
    chunks: list[dict],
    vectors: list[list[float]],
    window_counts: list[int],
) -> None:
    if not (len(chunks) == len(vectors) == len(window_counts)):
        raise ValueError("Chunk and embedding counts do not match")
    with sqlite3.connect(path) as database:
        database.execute(
            """
            CREATE TABLE IF NOT EXISTS chunk_embeddings (
                file TEXT NOT NULL,
                chunk_index INTEGER NOT NULL,
                start_line INTEGER NOT NULL,
                end_line INTEGER NOT NULL,
                symbols TEXT NOT NULL,
                estimated_tokens INTEGER NOT NULL,
                text TEXT NOT NULL,
                model_name TEXT NOT NULL,
                embedding TEXT NOT NULL,
                window_count INTEGER NOT NULL,
                PRIMARY KEY (file, chunk_index)
            )
            """
        )
        database.execute("DELETE FROM chunk_embeddings")
        database.executemany(
            """
            INSERT INTO chunk_embeddings
                (file, chunk_index, start_line, end_line, symbols,
                 estimated_tokens, text, model_name, embedding, window_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    chunk["file"],
                    chunk["chunk_index"],
                    chunk["start_line"],
                    chunk["end_line"],
                    json.dumps(chunk["symbols"], ensure_ascii=False),
                    chunk["estimated_tokens"],
                    chunk["text"],
                    MODEL_NAME,
                    json.dumps(vector, allow_nan=False),
                    window_count,
                )
                for chunk, vector, window_count in zip(chunks, vectors, window_counts)
            ],
        )


def main() -> None:
    chunks = read_chunks(CHUNKS_PATH)
    print(f"Loading {MODEL_NAME} to embed {len(chunks)} chunks...")
    model = SentenceTransformer(MODEL_NAME)
    vectors, window_counts = embed_chunks(chunks, model)
    save_embeddings(DATABASE_PATH, chunks, vectors, window_counts)
    print(
        f"Stored {len(vectors)} embeddings in {DATABASE_PATH} "
        f"({sum(window_counts)} token windows)."
    )


if __name__ == "__main__":
    main()
