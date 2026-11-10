# Task 4 Report: Embedding Matching

## Overview

`match_chunks.py` retrieves the *n* repository chunks most relevant to a query. The reusable function is `retrieve_top_n(query_embedding, n)`. Its command-line mode takes a text query, embeds it with the same model used in Task 3, and prints the top-*n* chunks (default `n = 5`).

Each result is a dictionary with `rank`, `similarity`, `file`, `start_line`, `end_line`, `symbols` and `text`.

## Design decisions

**SQLite, read-only.** The script reads the Task 3 database (`../Task_3/chunk_embeddings.db`) through a read-only SQLite connection (`mode=ro`), so retrieval cannot alter the stored data. Rows are loaded once into memory and cached for later calls in the same process. At 92 chunks, this is simple and fast.

**Compatibility checks.** While loading, the script verifies that every row uses `sentence-transformers/all-MiniLM-L6-v2`, has exactly 384 finite values, and has unit length. The query embedding must also be 384-dimensional, finite and non-zero. Comparing vectors from different models or sizes would give meaningless scores, so mismatches raise an error.

**Normalized vectors and cosine similarity.** Cosine similarity compares the direction of two vectors and ignores their length, which suits text embeddings. The stored vectors are already unit length (Task 3), and the script normalizes the query too. For unit vectors the cosine similarity equals the dot product, so one matrix-vector product, `embeddings @ query`, scores every chunk. Scores range from -1 to 1, and higher means more similar. Scaling a query vector does not change the results.

**Exact search.** The script scores every chunk instead of using an approximate index (such as a vector database). With 92 chunks this takes negligible time and always returns the true nearest chunks, with no extra dependencies or tuning.

**Top-n selection.** `numpy.argpartition` selects the *n* best scores without sorting all chunks. Only those *n* are then sorted by descending similarity; ties break by stored order, so results are deterministic.

**Validation of `n`.** `n` must be an integer of at least 1; other values raise `TypeError` or `ValueError` (the command-line option rejects values below 1). If `n` exceeds the number of chunks, all chunks are returned, ranked.

## Installation and execution

Requires Python 3. From the `Week_06_Implementation/Assignments/Task_4` folder:

```powershell
python -m pip install -r requirements.txt
python match_chunks.py "how are duplicate entities handled in the repository"
python match_chunks.py "calculate order total with discounts" -n 3
```

The Task 3 database must already exist (run `Task_3/embed_chunks.py` first). The first command-line run downloads the embedding model unless it is cached. Use from Python:

```python
from match_chunks import retrieve_top_n
results = retrieve_top_n(query_embedding, n=5)  # 384-dim vector, same model
```

## Testing

- **Queries.** Several queries were checked, for example "calculate order total with discounts" ranked `pricing.py` first, and "inventory stock reservation" ranked `inventory.py` first, followed by other reservation-related chunks.
- **Values of `n`.** `n` = 1, 2, 3, 5, 10, 91, 92 and 500 were tested; the default gave 5 results, and `-n 1000` returned all 92 chunks.
- **Exactness.** On three query vectors, the results matched a brute-force full sort of all scores for every tested `n`, and a stored vector (even scaled by 100) matched itself with similarity 1.
- **Validation.** Invalid `n` (0, negative, float, boolean), wrong-dimension, zero or non-finite queries, a missing database, and database copies with a different model name or vector size were all rejected.
- **Safety.** The connection rejects writes, and the Task 3 database file was unchanged (identical hash) after testing.
