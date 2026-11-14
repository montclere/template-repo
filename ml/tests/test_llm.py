import json

import pytest

from app.config import settings
from app.llm.client import LLMError, complete


def read_log(fake_llm) -> list[dict]:
    return [json.loads(line) for line in fake_llm.log_path.read_text().splitlines()]


def test_complete_returns_text_and_logs_the_call(fake_llm):
    assert complete("hi", system="be brief") == "hello"

    sent = fake_llm.requests[0]
    assert sent["path"] == "/v1/messages"
    assert sent["key"] == "test-key"
    assert sent["body"]["model"] == "test-model"
    assert sent["body"]["system"] == "be brief"

    record = read_log(fake_llm)[0]
    assert record["prompt"] == "hi"
    assert record["response"] == "hello"
    assert record["input_tokens"] == 3
    assert "test-key" not in fake_llm.log_path.read_text()


def test_complete_retries_when_the_api_is_overloaded(fake_llm):
    fake_llm.statuses = [529, 429]

    assert complete("hi") == "hello"
    assert len(fake_llm.requests) == 3


def test_complete_raises_and_logs_after_retries_run_out(fake_llm):
    fake_llm.statuses = [500, 500, 500]

    with pytest.raises(LLMError):
        complete("hi")

    assert len(fake_llm.requests) == 3
    assert "error" in read_log(fake_llm)[0]


def test_complete_does_not_retry_a_bad_request(fake_llm):
    fake_llm.statuses = [400]

    with pytest.raises(LLMError):
        complete("hi")

    assert len(fake_llm.requests) == 1


def test_complete_can_log_without_text(fake_llm, monkeypatch):
    monkeypatch.setattr(settings, "llm_log_text", False)

    complete("secret question")

    record = read_log(fake_llm)[0]
    assert "secret question" not in fake_llm.log_path.read_text()
    assert record["prompt_chars"] == len("secret question")


def test_complete_requires_model_and_key(fake_llm, monkeypatch):
    monkeypatch.setattr(settings, "anthropic_api_key", "")

    with pytest.raises(LLMError):
        complete("hi")
