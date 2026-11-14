import json
import time
import urllib.error
import urllib.request
from datetime import UTC, datetime
from pathlib import Path

from app.config import settings

RETRY_STATUSES = {429, 500, 502, 503, 504, 529}


class LLMError(RuntimeError):
    pass


def complete(prompt: str, *, system: str | None = None, max_tokens: int | None = None) -> str:
    if not settings.llm_model or not settings.anthropic_api_key:
        raise LLMError("LLM_MODEL and ANTHROPIC_API_KEY must be set in ml/.env")

    body: dict = {
        "model": settings.llm_model,
        "max_tokens": max_tokens or settings.llm_max_tokens,
        "messages": [{"role": "user", "content": prompt}],
    }
    if system:
        body["system"] = system

    record: dict = {
        "at": datetime.now(UTC).isoformat(),
        "model": settings.llm_model,
        **_loggable(system=system, prompt=prompt),
    }
    started = time.monotonic()
    try:
        payload = _post_with_retries(body)
        text = _extract_text(payload)
        usage = payload.get("usage", {})
        record.update(
            _loggable(response=text),
            input_tokens=usage.get("input_tokens"),
            output_tokens=usage.get("output_tokens"),
        )
        return text
    except LLMError as error:
        record["error"] = str(error)
        raise
    finally:
        record["latency_ms"] = round((time.monotonic() - started) * 1000)
        _write_log(record)


def _post_with_retries(body: dict) -> dict:
    attempts = settings.llm_max_retries + 1
    for attempt in range(attempts):
        is_last = attempt == attempts - 1
        try:
            return _post(body)
        except urllib.error.HTTPError as error:
            if error.code not in RETRY_STATUSES or is_last:
                detail = error.read().decode(errors="replace")
                raise LLMError(f"{error.code} {detail}") from error
        except (urllib.error.URLError, TimeoutError) as error:
            if is_last:
                raise LLMError(str(getattr(error, "reason", error))) from error
        time.sleep(settings.llm_retry_delay_seconds * 2**attempt)
    raise AssertionError("unreachable")


def _post(body: dict) -> dict:
    request = urllib.request.Request(
        f"{settings.llm_base_url}/v1/messages",
        data=json.dumps(body).encode(),
        method="POST",
        headers={
            "content-type": "application/json",
            "x-api-key": settings.anthropic_api_key,
            "anthropic-version": settings.llm_api_version,
        },
    )
    with urllib.request.urlopen(request, timeout=settings.llm_timeout_seconds) as response:
        raw = response.read()
    try:
        return json.loads(raw)
    except ValueError as error:
        raise LLMError("model API returned a non-JSON response") from error


def _extract_text(payload: dict) -> str:
    try:
        return "".join(b.get("text", "") for b in payload["content"] if b.get("type") == "text")
    except (KeyError, TypeError, AttributeError) as error:
        raise LLMError(f"unexpected model API response: {payload!r:.300}") from error


def _write_log(record: dict) -> None:
    path = Path(settings.llm_log_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as log:
        log.write(json.dumps(record, ensure_ascii=False) + "\n")


def _loggable(**fields: str | None) -> dict:
    if settings.llm_log_text:
        return fields
    return {f"{name}_chars": len(value or "") for name, value in fields.items()}
