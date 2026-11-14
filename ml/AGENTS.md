# ml

FastAPI service with all the AI: model calls, prompts, RAG, agents, MCP. Only the backend calls it. No `domain` layer: each capability is a module that takes input and returns output.

## Layout
- `config.py` — `Settings`: model, key, limits, timeouts, retries, log path.
- `llm/client.py` — `complete()`, the only place that calls the model API. `llm/prompts.py` — `load_prompt(name)` reads `prompts/<name>.md`.
- `ask/service.py` — the example capability: question in, answer out.
- `api/routes/`, `api/schemas/` — one route and one request/response schema per endpoint, `/api/v1/health` included.
- `prompts/` — prompts as files, never inline in code.
- `evals/` — `cases.jsonl` and the runner behind `make eval`.

## Adding a capability (RAG, an agent, a second endpoint)
- New sibling module next to `ask/` (`rag/`, `agent/`), its own route and schema. Replace or delete `ask/` when the real capability covers it.
- If it loads something heavy once (an index, weights), create it in `api/deps.py` behind `@lru_cache` and inject it with `Depends`.
- No shared base class until there are two real implementations that need one.
- An MCP server goes in `app/mcp/` as a thin wrapper over the sibling modules.
- Write eval cases for it in `evals/cases.jsonl` before the code. Topic guidance: `docs/playbooks/` (`agents`, `rag`, `mcp`, `evals`, `security`).

## Model calls
- `complete(prompt, system=..., max_tokens=...)` targets the Anthropic Messages API without an SDK. It retries 429/5xx/529 and timeouts (`LLM_MAX_RETRIES`), raises `LLMError` on failure, and appends every call to `logs/llm.log.jsonl` (prompt, response, latency, tokens; never the key; with `LLM_LOG_TEXT=false` only text lengths).
- It is synchronous: call it from a plain `def` route (FastAPI runs those in a thread pool).
- Routes turn `LLMError` into `502`.
- To switch provider or add streaming or tool use, change only `llm/client.py`. An SDK is a new dependency — ask first.

## Tests
- Plain functions, no classes. Hit HTTP routes through the `client` fixture.
- Tests never call the real model: the `fake_llm` fixture in `tests/conftest.py` starts a local fake API. Set `fake_llm.reply_text`, queue error codes in `fake_llm.statuses`, read sent requests from `fake_llm.requests`. Copy the pattern from `tests/test_ask.py`.

## Commands
- `uv run uvicorn app.main:app --reload --port 8100`
- `uv run ruff format . && uv run ruff check .`
- `uv run pytest`
