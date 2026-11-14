---
name: clean-architecture
description: Design a new backend or ml module, or review a diff for layer and dependency problems, using this repo's layering. Use when designing a new feature slice, when asked for an architecture or dependency review, or when unsure which layer code belongs in.
---

# Clean architecture in this repo

The goal is code that is easy to change and to test with fakes, not the maximum number of layers. Adding a layer the current task does not use is a defect, the same as a missing one.

## The dependency rule

Source code dependencies point inward only.

| Service | Layers (outer → inner) |
| --- | --- |
| `backend` | `api` (routes, schemas, deps) → `services` → `domain` ← `infra` (db, `ml_client`) |
| `ml` | `api` → capability modules (`ask/`, `rag/`, `agent/`) → `llm/` |
| `frontend` | `app/` → `features/<name>/` → `shared/` |

- `domain` imports nothing from the project except other `domain` modules, and no frameworks.
- `services` depend on `Protocol`s from `domain`, never on `infra` classes. The concrete class is chosen in `api/deps.py`.
- Schemas (`api/schemas/`) never leave `api/`. Routes convert schema ↔ entity.
- Only `infra` (backend) and `llm/client.py` (ml) talk to databases and external APIs.
- Services never import each other's code; they share only HTTP contracts.

## Designing a new feature

1. Write the HTTP contract (schemas) first.
2. Backend slice, in this order, skipping what has nothing to hold: entity + `Protocol`s in `domain/<feature>.py` → service → `infra` implementation → schema → route → wiring in `deps.py` → test through the route.
3. A pure pass-through to `ml` may skip the service; add it as soon as logic appears.
4. A `Protocol` is justified when tests need a fake or there really are two implementations.

## Review checklist

Report each finding as `file:line — problem — fix`.

- Inner layer imports an outer one (e.g. `domain` imports SQLAlchemy, a service imports `infra`, a schema used in a service).
- Business logic in a route; HTTP or SQL details in a service.
- Hardcoded URL, key, model name, threshold, limit or timeout instead of `Settings`.
- `os.getenv` outside `config.py`.
- A layer, class, `Protocol`, parameter or option nothing uses yet.
- The same logic in two places.
- Functions doing more than one thing; names that don't say what the function does.
- Missing route-level test for new behaviour.

End with the 1–3 changes that matter most. Don't rewrite code during a review unless asked.
