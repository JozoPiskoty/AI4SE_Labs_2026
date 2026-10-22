from __future__ import annotations

import hashlib
import json
import logging
import os
import tempfile
from pathlib import Path
from typing import Any

from .models import ConsolidationResult, ExtractionResult


LOGGER = logging.getLogger("requirements_agent")
CACHE_SCHEMA_VERSION = 1


class ExtractionCache:
    def __init__(self, output_dir: Path):
        self.path = output_dir / ".cache" / "extraction_cache.json"
        self.entries: dict[str, dict[str, Any]] = {}
        if not self.path.exists():
            return
        try:
            payload = json.loads(self.path.read_text(encoding="utf-8"))
            if payload.get("schema_version") != CACHE_SCHEMA_VERSION:
                LOGGER.warning("Cache extrakcie má nekompatibilnú verziu; vytváram novú.")
                return
            entries = payload.get("entries", {})
            if isinstance(entries, dict):
                self.entries = entries
            else:
                LOGGER.warning("Cache extrakcie má neplatný formát; vytváram novú.")
        except (OSError, json.JSONDecodeError, AttributeError) as exc:
            LOGGER.warning(
                "Cache extrakcie sa nepodarilo načítať (%s); úspešné dávky sa vytvoria nanovo.",
                type(exc).__name__,
            )

    @staticmethod
    def fingerprint(
        model_name: str,
        prompt_version: str,
        documents: list[dict[str, Any]],
        prompt_context: str,
    ) -> str:
        material = json.dumps(
            {
                "model": model_name,
                "prompt_version": prompt_version,
                "prompt_context": prompt_context,
                "documents": [
                    {"id": doc["id"], "name": doc["name"], "text": doc["text"]}
                    for doc in documents
                ],
            },
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        return hashlib.sha256(material.encode("utf-8")).hexdigest()

    def get(
        self,
        model_name: str,
        prompt_version: str,
        documents: list[dict[str, Any]],
        prompt_context: str = "",
    ) -> ExtractionResult | None:
        fingerprint = self.fingerprint(model_name, prompt_version, documents, prompt_context)
        entry = self.entries.get(fingerprint)
        if entry is None:
            return None
        if (
            entry.get("model") != model_name
            or entry.get("prompt_version") != prompt_version
            or entry.get("input_fingerprint") != fingerprint
            or entry.get("prompt_context_fingerprint")
            != hashlib.sha256(prompt_context.encode("utf-8")).hexdigest()
        ):
            return None
        try:
            return ExtractionResult.model_validate(entry["result"])
        except (KeyError, ValueError, TypeError) as exc:
            LOGGER.warning(
                "Cache položka %s je neplatná (%s); dávka sa spracuje znova.",
                fingerprint[:12],
                type(exc).__name__,
            )
            return None

    def put(
        self,
        model_name: str,
        prompt_version: str,
        documents: list[dict[str, Any]],
        result: ExtractionResult,
        prompt_context: str = "",
    ) -> None:
        fingerprint = self.fingerprint(model_name, prompt_version, documents, prompt_context)
        self.entries[fingerprint] = {
            "model": model_name,
            "prompt_version": prompt_version,
            "input_fingerprint": fingerprint,
            "prompt_context_fingerprint": hashlib.sha256(prompt_context.encode("utf-8")).hexdigest(),
            "result": result.model_dump(mode="json"),
        }
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=self.path.parent,
                prefix="extraction_cache_",
                suffix=".tmp",
                delete=False,
            ) as temporary_file:
                temporary_path = Path(temporary_file.name)
                json.dump(
                    {"schema_version": CACHE_SCHEMA_VERSION, "entries": self.entries},
                    temporary_file,
                    ensure_ascii=False,
                    indent=2,
                )
                temporary_file.flush()
                os.fsync(temporary_file.fileno())
            temporary_path.replace(self.path)
        except OSError:
            if temporary_path is not None:
                temporary_path.unlink(missing_ok=True)
            raise


class ConsolidationCache:
    def __init__(self, output_dir: Path):
        self.path = output_dir / ".cache" / "consolidation_cache.json"
        self.entries: dict[str, dict[str, Any]] = {}
        if not self.path.exists():
            return
        try:
            payload = json.loads(self.path.read_text(encoding="utf-8"))
            if payload.get("schema_version") != CACHE_SCHEMA_VERSION:
                LOGGER.warning("Cache konsolidácie má nekompatibilnú verziu; vytváram novú.")
                return
            entries = payload.get("entries", {})
            if isinstance(entries, dict):
                self.entries = entries
            else:
                LOGGER.warning("Cache konsolidácie má neplatný formát; vytváram novú.")
        except (OSError, json.JSONDecodeError, AttributeError) as exc:
            LOGGER.warning(
                "Cache konsolidácie sa nepodarilo načítať (%s); skupiny sa spracujú znova.",
                type(exc).__name__,
            )

    @staticmethod
    def _fingerprint(
        model_name: str,
        prompt_version: str,
        candidates: list[dict[str, Any]],
        prompt_context: str,
    ) -> str:
        material = json.dumps(
            {
                "model": model_name,
                "prompt_version": prompt_version,
                "prompt_context": prompt_context,
                "candidates": candidates,
            },
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        return hashlib.sha256(material.encode("utf-8")).hexdigest()

    def get(
        self,
        model_name: str,
        prompt_version: str,
        candidates: list[dict[str, Any]],
        prompt_context: str,
    ) -> ConsolidationResult | None:
        fingerprint = self._fingerprint(model_name, prompt_version, candidates, prompt_context)
        entry = self.entries.get(fingerprint)
        if entry is None:
            return None
        if (
            entry.get("model") != model_name
            or entry.get("prompt_version") != prompt_version
            or entry.get("input_fingerprint") != fingerprint
        ):
            return None
        try:
            return ConsolidationResult.model_validate(entry["result"])
        except (KeyError, ValueError, TypeError) as exc:
            LOGGER.warning(
                "Cache skupiny %s je neplatná (%s); skupina sa spracuje znova.",
                fingerprint[:12],
                type(exc).__name__,
            )
            return None

    def put(
        self,
        model_name: str,
        prompt_version: str,
        candidates: list[dict[str, Any]],
        prompt_context: str,
        result: ConsolidationResult,
    ) -> None:
        fingerprint = self._fingerprint(model_name, prompt_version, candidates, prompt_context)
        self.entries[fingerprint] = {
            "model": model_name,
            "prompt_version": prompt_version,
            "input_fingerprint": fingerprint,
            "result": result.model_dump(mode="json"),
        }
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=self.path.parent,
                prefix="consolidation_cache_",
                suffix=".tmp",
                delete=False,
            ) as temporary_file:
                temporary_path = Path(temporary_file.name)
                json.dump(
                    {"schema_version": CACHE_SCHEMA_VERSION, "entries": self.entries},
                    temporary_file,
                    ensure_ascii=False,
                    indent=2,
                )
                temporary_file.flush()
                os.fsync(temporary_file.fileno())
            temporary_path.replace(self.path)
        except OSError:
            if temporary_path is not None:
                temporary_path.unlink(missing_ok=True)
            raise
