# Requirements refinement network

Python/LangGraph pipeline that extracts, consolidates, reviews, and validates
software requirements from `.txt` and `.eml` source documents.

## Setup

From this directory, create and activate a virtual environment, then install
the dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Set `OPENAI_API_KEY` in the current process environment, or copy `.env.example`
to `.env` and set the key there. `.env` is loaded locally and ignored by Git.
Alternatively, if no key is configured, the program securely prompts for one
using hidden terminal input. It never saves an interactively entered key.

If the provider requires a custom endpoint, set `OPENAI_BASE_URL`. The three
model IDs can be changed using `REQ_MODEL_EXTRACTION`,
`REQ_MODEL_CONSOLIDATION`, and `REQ_MODEL_REVIEW`. Defaults are
`gpt-5.4-nano` for extraction, `gpt-5-mini` for consolidation, and
`gpt-5-nano` for review. The program requires three distinct IDs, checks
each model with a small request, and does not silently substitute models.

## Run

```powershell
python main.py --input-dir .\data\corpus --output-dir .\output
```

The input directory is scanned recursively. `.txt` and `.eml` are supported;
email headers such as sender, recipients, subject, and date are retained.
Outputs are `requirements.md` and `run_summary.json`. Set
`--max-iterations` to configure the feedback repair limit (default: 1; only 0 or 1 is allowed).
`--extraction-batch-chars` configures the maximum source text size per
extraction batch (default: 12000 characters).
`--consolidation-batch-size` sets the maximum number of candidates sent to
one local consolidation request (default: 45).
Timestamped progress logs are written to the terminal for loading, per-model
preflight checks, each LLM node and batch, review retries, validation, and
output writing. API calls use a 90-second timeout and one SDK retry;
calls that exceed the wait-warning threshold emit a warning and continue
waiting for the response. Prompts, document contents, and API keys are not
included in progress logs.

Each successful extraction batch is atomically saved to
`<output-dir>\.cache\extraction_cache.json`. Later runs reuse a batch only
when its exact source names/content, extraction model ID, and extraction
prompt version and review-feedback context match. The cache contains
extraction results, never the API key. If a later batch fails, earlier
successful batch results remain cached
and are reused on retry. `requirements.md` and `run_summary.json` are written
only after the complete graph finishes successfully; a failed graph run does
not produce a partial requirements document. API requests have a 90-second
timeout and one SDK retry, so retries remain bounded.

Consolidation uses one pass over bounded groups, then one global audit of the
compact candidate and requirement indexes to detect cross-group duplicates,
conflicts, source coverage, and completeness. It does not run repeated
hierarchical consolidation stages. Each successful local or targeted repair
group is saved to `<output-dir>\.cache\consolidation_cache.json`. Cache reuse
requires matching candidate data, model ID, prompt version, phase/group,
source manifest, and feedback context. The consolidation prompt/cache version
was incremented so incompatible results from the previous algorithm are not
reused; extraction cache compatibility is preserved.

Consolidated items carry deterministic internal candidate references. Their
source documents and evidence are derived only from the referenced original
candidates; model-returned source strings are never added to the provenance.
E-mail addresses found in source references are resolved against e-mail
headers, with unique evidence matches as a fallback. Unresolvable sources are
omitted rather than guessed, and the requirement is marked for manual review
with a validation warning. These warnings are included in both final outputs
but do not prevent output generation. Any candidate omitted from both accepted
and rejected model results is retained rather than silently dropped. If review identifies precisely scoped, repairable targets,
the graph performs at most one targeted repair pass and reviews the result
once more. Unresolved or unscoped findings are preserved for human review.
Deterministic validation failures stop the run before either final output file
is written.

The targeted repair step preserves the original draft/final requirement ID
where the repaired result still represents that requirement, and reattaches
its sources and evidence from candidate references. Existing extraction
results remain reusable. Consolidation cache entries are also reusable when
the original candidate inputs match; provenance is normalized after cache
retrieval, so prior model-returned e-mail addresses are corrected without
repeating successful consolidation calls.

For 368 extracted candidates and the default group size of 45, a cache-cold
run requires about 9 local consolidation calls and 1 global review call; a
targeted repair adds calls only for affected groups (usually 0–1), followed by
one review call. Preflight adds 3 calls, and extraction calls depend on the
number of source batches not already cached. These are estimates; no live
corpus run is implied.

## Tests

Run the offline tests from this directory:

```powershell
python -m unittest discover -s tests -v
```

The tests use fake model responses and do not contact the API.
