.PHONY: help env up logs backend-dev backend-lint backend-test frontend-dev frontend-lint ml-dev ml-lint ml-test lint test check smoke eval typecheck hooks

help:
	@echo "run these from the repo root"
	@echo ""
	@echo "  make env            - copy .env.example -> .env everywhere it's missing"
	@echo ""
	@echo "  make up             - full stack via docker (builds automatically)"
	@echo "  make logs           - follow docker logs"
	@echo ""
	@echo "  make backend-dev    - run backend without docker (deps installed automatically)"
	@echo "  make frontend-dev   - run frontend without docker (deps installed automatically)"
	@echo "  make ml-dev         - run ml without docker (deps installed automatically)"
	@echo ""
	@echo "  make lint           - format + lint all services"
	@echo "  make test           - run backend + ml test suites"
	@echo "  make check          - lint + test, run before calling a task done"
	@echo "  make smoke          - end-to-end check against the running stack"
	@echo "  make eval           - evals for the LLM part (ml must be running)"
	@echo "  make typecheck      - mypy for backend + ml (downloads mypy on first run)"
	@echo "  make hooks          - install git pre-commit hooks (lint+format before each commit)"

env:
	@for dir in . backend frontend ml; do \
		[ -d $$dir ] && [ ! -f $$dir/.env ] && cp $$dir/.env.example $$dir/.env && echo "created $$dir/.env"; \
	done; true

up:
	docker compose up --build

logs:
	docker compose logs -f

backend-dev:
	cd backend && uv run uvicorn app.main:app --reload --port 8000

backend-lint:
	cd backend && uv run ruff format . && uv run ruff check .

backend-test:
	cd backend && uv run pytest

frontend-dev:
	cd frontend && npm install && npm run dev

frontend-lint:
	cd frontend && npm run format && npm run lint

ml-dev:
	cd ml && uv run uvicorn app.main:app --reload --port 8100

ml-lint:
	cd ml && uv run ruff format . && uv run ruff check .

ml-test:
	cd ml && uv run pytest

lint: backend-lint frontend-lint ml-lint

test: backend-test ml-test

check: lint test

smoke:
	bash scripts/smoke.sh

eval:
	cd ml && uv run python -m evals.run

typecheck:
	cd backend && uv run --with mypy mypy app --ignore-missing-imports --explicit-package-bases
	cd ml && uv run --with mypy mypy app evals --ignore-missing-imports --explicit-package-bases

hooks:
	uvx pre-commit install
