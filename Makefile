DEV  := -f compose.yaml -f compose.dev.yaml
PROD := -f compose.yaml -f compose.prod.yaml

.PHONY: up down build logs shell test cov migrate revision \
        prod-up prod-down prod-build prod-logs


up:
	docker compose $(DEV) up --build

down:
	docker compose $(DEV) down

build:
	docker compose $(DEV) build

logs:
	docker compose $(DEV) logs -f

shell:
	docker compose $(DEV) exec api bash


test:
	docker compose $(DEV) run --rm api pytest

cov:
	docker compose $(DEV) run --rm api pytest
	open htmlcov/index.html || xdg-open htmlcov/index.html


migrate:       ## Apply all pending migrations
	docker compose $(DEV) run --rm api alembic upgrade head

revision:      ## Generate a new migration: make revision msg="add users table"
	docker compose $(DEV) run --rm api alembic revision --autogenerate -m "$(msg)"


prod-up:
	docker compose $(PROD) up --build -d

prod-down:
	docker compose $(PROD) down

prod-build:
	docker compose $(PROD) build

prod-logs:
	docker compose $(PROD) logs -f
