# backend

FastAPI service: stores data and is the only API the frontend calls. Reaches `ml` over HTTP.

## Layers
Dependencies point inward: `api` → `services` → `domain` ← `infra`. `domain` and `services` never import FastAPI, SQLAlchemy or HTTP code.

- `config.py` — `Settings`. Components get values as constructor args from `api/deps.py`; nothing else reads env vars.
- `domain/<feature>.py` — dataclass entities, `Protocol`s for what the feature needs from outside (repository, `Assistant`), and domain errors. Plain Python.
- `services/<feature>_service.py` — the logic. Takes the `Protocol`s in its constructor.
- `infra/` — implementations: `db/` (SQLAlchemy models, session, repositories), `ml_client.py` (HTTP client for `ml`).
- `api/` — `routes/`, `schemas/` (request/response DTOs, used only inside `api/`), `deps.py` (wiring via `Depends`). Routes convert schemas ↔ entities and map domain errors to HTTP codes.
- `main.py` — composition root: creates the app, includes routers, calls `init_db()`.

The example slice is `questions`: `domain/question.py` → `services/question_service.py` → `infra/db/question_repository.py` + `infra/ml_client.py` → `api/routes/questions.py`.

## When to add a layer
- A feature with data or logic gets the full slice, in the order above.
- A plain pass-through (a route that only forwards to `ml` and returns the result) may call an `infra` client from the route through `deps.py`. Add a service the moment there is logic.
- No `Protocol` for something nobody needs to swap or fake in tests.

## Constraints
- No migrations: `init_db()` runs `create_all` on startup. Changing a model on an existing database means dropping it (`docker compose down -v`). Add Alembic if the project outlives the hackathon.
- `DATABASE_URL` defaults to sqlite for local dev; docker-compose sets postgres. `ML_URL` defaults to `http://localhost:8100`; docker-compose sets `http://ml:8000`.

## Tests
- Plain functions, no classes. Hit HTTP routes through the `client` fixture, assert on status code and JSON body.
- `tests/conftest.py` points `DATABASE_URL` at a throwaway sqlite file and replaces `ml` with `FakeAssistant` (fixture `assistant`; set `assistant.down = True` to simulate an outage). Tests never call the real `ml`.
- New test: `tests/test_<thing>.py`, copy the pattern from `tests/test_questions.py`.

## Commands
- `uv run uvicorn app.main:app --reload` (installs deps automatically)
- `uv run ruff format . && uv run ruff check .`
- `uv run pytest`
