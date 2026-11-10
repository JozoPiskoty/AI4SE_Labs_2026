# Task 3 Report: Chunk Embeddings

## Overview

`embed_chunks.py` reads the 92 chunks from `../Task_2/repository_chunks.jsonl`, embeds each chunk's original text, and stores the chunks with their embeddings in `chunk_embeddings.db`. Similarity search is not implemented here.

## Embedding model

The script uses `sentence-transformers/all-MiniLM-L6-v2`, a compact model that runs locally and needs no remote embedding API. It produces **384-dimensional** vectors, which the script checks before embedding.

## Long chunks

The model accepts at most 256 WordPiece tokens, including the `[CLS]` and `[SEP]` special tokens. The script tokenizes each chunk without truncation and splits the token IDs into non-overlapping windows of up to 254 content tokens, which leaves room for the special tokens. Each window is embedded separately, and the window embeddings for a chunk are averaged. No input text is silently truncated.

## Normalization

After averaging, each chunk's vector is L2-normalized to unit length. The script rejects any zero-length or non-finite vector, so each stored embedding is a finite unit vector.

## SQLite storage

Data is stored in the `chunk_embeddings` table of `chunk_embeddings.db`. The primary key is `(file, chunk_index)`, which preserves chunk identifiers. Each row contains:

- `file`, `chunk_index`, `start_line`, `end_line`
- `symbols` (JSON array) and `estimated_tokens`
- `text` (the original chunk text)
- `model_name`
- `embedding` (JSON array of 384 floats)
- `window_count` (number of token windows used for the chunk)

Re-running the script replaces the existing rows in a single transaction. SQLite is sufficient for this small dataset and needs no separate server.

## Verification

- 92 embeddings were generated from 92 chunks, using 243 token windows in total (at most 4 windows for one chunk).
- The database integrity check passed, and every row matched its source chunk's metadata and text.
- Every embedding has 384 finite values and unit length (maximum norm error about 2.2e-16).
- An independent recomputation for the chunk with the most windows (784 WordPiece tokens in 4 windows) matched the stored averaged embedding.

## Installation and execution

Requires Python 3 and the dependency in `requirements.txt` (`sentence-transformers>=3.0,<6.0`, which also installs PyTorch and Transformers). From the `Week_06_Implementation/Assignments/Task_3` folder:

```powershell
python -m pip install -r requirements.txt
python embed_chunks.py
```

The first run downloads the model from the Hugging Face Hub, so it needs internet access; later runs can use the local cache. The script writes `chunk_embeddings.db` in the same folder.
