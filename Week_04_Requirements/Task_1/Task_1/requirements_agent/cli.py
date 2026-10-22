from __future__ import annotations

import argparse
import getpass
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from .models import ConsolidationResult, ExtractionResult, ReviewResult
from .network import build_graph
from .progress import (
    LOGGER,
    configure_logging,
    safe_error_message,
    timed_invoke,
)
from .reporting import write_outputs


DEFAULT_MODELS = {
    "extraction": "gpt-5.4-nano",
    "consolidation": "gpt-5-mini",
    "review": "gpt-5-nano",
}
MODEL_ENV = {
    "extraction": "REQ_MODEL_EXTRACTION",
    "consolidation": "REQ_MODEL_CONSOLIDATION",
    "review": "REQ_MODEL_REVIEW",
}


def _get_api_key() -> str:
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if key:
        return key
    if not sys.stdin.isatty():
        raise RuntimeError(
            "OPENAI_API_KEY is not configured and no interactive terminal is available. "
            "Set OPENAI_API_KEY in your process environment and run the command again."
        )
    key = getpass.getpass("OpenAI API key (input hidden): ").strip()
    if not key:
        raise RuntimeError("The API key cannot be empty.")
    os.environ["OPENAI_API_KEY"] = key
    return key


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Refine software requirements from a text corpus.")
    parser.add_argument("--input-dir", type=Path, default=Path("data/corpus"))
    parser.add_argument("--output-dir", type=Path, default=Path("output"))
    parser.add_argument(
        "--max-iterations",
        type=int,
        choices=(0, 1),
        default=1,
        help="Allow at most one targeted corrective pass (default: 1).",
    )
    parser.add_argument(
        "--extraction-batch-chars",
        type=int,
        default=12000,
        help="Maximum source text characters in each extraction batch (default: 12000).",
    )
    parser.add_argument(
        "--consolidation-batch-size",
        type=int,
        default=45,
        help="Maximum candidate requirements per consolidation request (default: 45).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    load_dotenv(override=False)
    configure_logging()
    args = _parse_args(argv)
    LOGGER.info("Spúšťam agentickú sieť.")
    LOGGER.info("Vstupný priečinok: %s", args.input_dir)
    LOGGER.info("Výstupný priečinok: %s", args.output_dir)
    if args.max_iterations < 0:
        print("--max-iterations must be zero or greater.", file=sys.stderr)
        return 2
    if args.extraction_batch_chars < 1:
        print("--extraction-batch-chars must be greater than zero.", file=sys.stderr)
        return 2
    if args.consolidation_batch_size < 1:
        print("--consolidation-batch-size must be greater than zero.", file=sys.stderr)
        return 2
    models = {
        role: os.environ.get(MODEL_ENV[role], default)
        for role, default in DEFAULT_MODELS.items()
    }
    if len(set(models.values())) != len(models):
        print("Extraction, consolidation, and review must use three different model IDs.", file=sys.stderr)
        return 2
    try:
        api_key = _get_api_key()
    except RuntimeError as exc:
        LOGGER.error("%s", safe_error_message(exc))
        return 2

    endpoint = os.environ.get("OPENAI_BASE_URL")
    common = {"api_key": api_key, "max_retries": 1, "timeout": 90}
    if endpoint:
        common["base_url"] = endpoint
    try:
        clients = {
            role: ChatOpenAI(model=model_id, **common)
            for role, model_id in models.items()
        }
        for role, client in clients.items():
            LOGGER.info("Kontrolujem dostupnosť modelu %s.", models[role])
            timed_invoke(
                client,
                "Reply with the single word READY.",
                node="predbežná kontrola",
                model_name=models[role],
                secret=api_key,
            )
    except Exception as exc:
        LOGGER.error(
            "Predbežná kontrola API/modelu zlyhala (%s): %s. "
            "Skontrolujte OPENAI_API_KEY, nakonfigurované ID modelov a OPENAI_BASE_URL "
            "(ak poskytovateľ vyžaduje vlastný endpoint). Modely sa automaticky nenahrádzajú.",
            type(exc).__name__,
            safe_error_message(exc, api_key),
        )
        return 1

    try:
        LOGGER.info("Pripravujem LangGraph pracovný tok.")
        graph = build_graph(
            clients["extraction"].with_structured_output(ExtractionResult),
            clients["consolidation"].with_structured_output(ConsolidationResult),
            clients["review"].with_structured_output(ReviewResult),
            model_names=models,
            api_secret=api_key,
            consolidation_batch_size=args.consolidation_batch_size,
        )
        state = graph.invoke({
            "input_dir": str(args.input_dir),
            "output_dir": str(args.output_dir),
            "max_iterations": args.max_iterations,
            "extraction_batch_chars": args.extraction_batch_chars,
            "consolidation_batch_size": args.consolidation_batch_size,
        })
        if state.get("validation_errors"):
            raise RuntimeError(
                "Deterministic validation failed: "
                + "; ".join(state["validation_errors"])
            )
        LOGGER.info("Zapisujem výsledné dokumenty.")
        write_outputs(state, args.input_dir, args.output_dir)
    except Exception as exc:
        LOGGER.error(
            "Spracovanie zlyhalo (%s): %s",
            type(exc).__name__,
            safe_error_message(exc, api_key),
        )
        return 1

    LOGGER.info(
        "Hotovo. Výsledný dokument: %s",
        args.output_dir / "requirements.md",
    )
    LOGGER.info(
        "Spracovaných %d dokumentov; vytvorených %d požiadaviek; %d validačných upozornení.",
        len(state.get("manifest", [])),
        len(state.get("requirements", [])),
        len(state.get("validation_errors", [])),
    )
    return 0
