.PHONY: *

DEV  := -f compose.yaml -f compose.dev.yaml
PROD := -f compose.yaml -f compose.prod.yaml

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

redis-cli:
	docker compose $(DEV) exec redis redis-cli

psql:
	docker compose $(DEV) exec postgres psql -U postgres


test:
	docker compose $(DEV) run --rm api pytest


migrate:
	docker compose $(DEV) run --rm api alembic upgrade head

revision:
	docker compose $(DEV) run --rm api alembic revision --autogenerate -m "$(msg)"


prod-up:
	docker compose $(PROD) up --build -d

prod-down:
	docker compose $(PROD) down

prod-build:
	docker compose $(PROD) build

prod-logs:
	docker compose $(PROD) logs -f
