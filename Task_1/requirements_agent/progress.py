from __future__ import annotations

import logging
import re
import sys
import threading
import time
from typing import Any


LOGGER = logging.getLogger("requirements_agent")
WAIT_WARNING_SECONDS = 20

_BEARER_PATTERN = re.compile(r"(?i)(bearer\s+)\S+")
_CREDENTIAL_PATTERN = re.compile(r"(?i)((?:api[_-]?key|authorization)\s*[:=]\s*)\S+")
_API_TOKEN_PATTERN = re.compile(r"\b(?:sk|rk|sess|sk-proj)-[A-Za-z0-9_-]{8,}\b")


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stderr,
        force=True,
    )


def safe_error_message(exc: Exception, secret: str | None = None) -> str:
    message = str(exc)
    if secret:
        message = message.replace(secret, "[REDACTED]")
    message = _BEARER_PATTERN.sub(r"\1[REDACTED]", message)
    message = _CREDENTIAL_PATTERN.sub(r"\1[REDACTED]", message)
    message = _API_TOKEN_PATTERN.sub("[REDACTED]", message)
    message = " ".join(message.split())
    return message[:400] or "No error details provided."


def timed_invoke(
    model: Any,
    prompt: str,
    *,
    node: str,
    model_name: str,
    batch: str | None = None,
    warning_after: float = WAIT_WARNING_SECONDS,
    secret: str | None = None,
) -> Any:
    context = f"uzol {node}, model {model_name}"
    if batch:
        context += f", {batch}"
    LOGGER.info("Volám API: %s.", context)
    started = time.perf_counter()
    warning = threading.Timer(
        warning_after,
        lambda: LOGGER.warning("Stále čakám na odpoveď API: %s.", context),
    )
    warning.daemon = True
    warning.start()
    try:
        result = model.invoke(prompt)
    except Exception as exc:
        elapsed = time.perf_counter() - started
        LOGGER.error(
            "API volanie zlyhalo (%s) po %.1f s: %s: %s",
            context,
            elapsed,
            type(exc).__name__,
            safe_error_message(exc, secret),
        )
        raise
    finally:
        warning.cancel()
    elapsed = time.perf_counter() - started
    LOGGER.info("API odpovedalo: %s za %.1f s.", context, elapsed)
    return result
