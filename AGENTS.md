# <project name>: <one line — what it is and for whom>

Three services, connected only over HTTP: `frontend/` (Vite + React) → `backend/` (FastAPI + Postgres) → `ml/` (FastAPI; all LLM, agent, RAG and MCP code lives here). The frontend talks only to the backend; the model API key lives only in `ml`. Each service has its own `AGENTS.md` — read it when you work there.

The template ships one end-to-end example: a question typed in the frontend goes to `POST /api/v1/questions` (backend saves it), the backend calls `POST /api/v1/ask` in `ml`, and `ml` calls the model with the prompt from `ml/prompts/ask.md`. Copy its shape for new features; replace or delete it once the real feature exists.

## Commands (run from the repo root)
- `make env` — create `.env` files from the examples
- `make up` / `make logs` — full stack in docker
- `make backend-dev` / `make frontend-dev` / `make ml-dev` — one service without docker
- `make check` — format + lint + tests for all services
- `make smoke` — end-to-end check against the running stack
- `make eval` — evals for the LLM part (needs `ml` running and a model key)

## Session start
Read the "Состояние" block in `docs/PROGRESS.md`, run `git log -5 --oneline`, then open your task in `docs/BRIEF.md`.

## Hard rules
1. Secrets live only in `.env` files. Never read, print or commit them.
2. Fix the HTTP contract (typed schema in the owning service) before code is written on either side. Never import code across services.
3. Before saying "done": run `make check` and show the output. If the change crosses services, also `make smoke`. If it touches prompts, retrieval or agent tools, also `make eval`.
4. After a task: tick it in `docs/BRIEF.md`, rewrite the "Состояние" block in `docs/PROGRESS.md` (including 1–3 things that could be better), then make one local commit named `T<n>: <what was done>`.

## Never without asking
- `git push`, creating or switching branches, rebase, reset, force, amending earlier commits.
- Adding a dependency, an external service, or anything that costs money.
- Editing `docs/input/`, the approved sections of the brief or a task's "готово, когда"; changing `Makefile`, docker, CI or `.env` files.
- Deleting files or data outside the current task; skipping or disabling a failing check.
If one of these seems needed, stop, say why, and offer options.

## Code quality
- No hardcoded values: URLs, keys, model names, thresholds, limits and timeouts come from `Settings`.
- One function does one thing; names say what it does.
- Routes hold no logic; logic knows nothing about HTTP or the database.
- The second time the same logic appears, extract it.
- Before "done", reread your own diff and delete what is not needed.
- When the brief lists judging criteria, don't do a task that maps to none of them — move it to "Не делаем".

## Defaults (deviate when you have a reason, and say why)
- MVP scope: add a layer, abstraction or dependency only when the current task uses it. Don't create folders "for later". The service `AGENTS.md` files say which layers exist and when to add one.
- When a contract changes, rewrite the schema; don't add optional fields for consumers that don't exist.
- Every endpoint returns a typed schema, health checks included.
- No comments in code except for a non-obvious constraint or workaround.
- Look for an existing library before writing your own. Check current library docs through Context7, not from memory.
- For decisions that are expensive to reverse (data model, whether RAG or an agent is needed at all, external services), offer 2–3 options with trade-offs. For everything else, decide and move on.
- When you ask the user something, give 2–3 options, recommend one and say why in a line.
- Before starting a task, write its steps under it in the brief, grouped by part: contract, ml, backend, frontend, check.
- If you see a better path than the brief describes, write it to "Идеи и сомнения" in `docs/PROGRESS.md` and tell the user.
- Start a new session when the topic changes or the context fills up, not after every task.

## Where things are
- `docs/input/` — hackathon description, judging criteria, the idea, organizer materials. Never edit these.
- `docs/BRIEF.md` — the one-page plan: judging criteria, demo scenario, contract, tasks.
- `docs/PROGRESS.md` — current state and open ideas.
- `docs/playbooks/` — `agents`, `rag`, `mcp`, `evals`, `security`. Read one only when the task is about that topic.
- `docs/long-project/` — SPEC, PLAN and TASKS templates, only for projects longer than three days.
- `.agents/skills/` — `feature-interview`, `task-breakdown`, `clean-architecture`, `frontend-design`, `diagnosing-bugs`, `mcp-builder` (`.claude/skills` is a symlink to it).
