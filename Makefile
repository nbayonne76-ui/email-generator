.PHONY: help install dev-backend dev-frontend db-init seed lint format test check

help:
	@grep -E '^[a-z-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "}{printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

install: ## Installe backend (venv) + frontend
	cd backend && (test -d venv || python3 -m venv venv) && ./venv/bin/pip install -q -r requirements-dev.txt
	cd frontend && npm install

dev-backend: ## uvicorn sur 8001 (règle H'appi WSL2)
	cd backend && ./venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload

dev-frontend: ## vite sur 5173
	cd frontend && npm run dev

db-init: ## Crée la base et les tables (provisoire, à remplacer par Alembic)
	PGPASSWORD=postgres psql -U postgres -h localhost -f database/scripts/init.sql

seed: ## Charge les données de démo (idempotent)
	PGPASSWORD=postgres psql -U postgres -h localhost -d development_db -f database/seeds/sample_data.sql

lint: ## ruff + oxlint
	cd backend && ./venv/bin/ruff check . && ./venv/bin/ruff format --check .
	cd frontend && npm run lint

format: ## ruff format + corrections automatiques
	cd backend && ./venv/bin/ruff format . && ./venv/bin/ruff check . --fix

test: ## pytest
	cd backend && ./venv/bin/pytest -q

check: lint test ## Tout valider avant de considérer une tâche terminée
	cd frontend && npm run build
	@echo "✅ lint + tests + build OK"
