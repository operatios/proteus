# Used https://docs.astral.sh/uv/guides/integration/docker/ as reference

# base
FROM python:3.14-slim AS base

ENV UV_PYTHON_DOWNLOADS=never
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app

EXPOSE 8000

# builder
FROM base AS builder

COPY --from=ghcr.io/astral-sh/uv:0.11.32 /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

COPY pyproject.toml uv.lock .

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project

COPY app ./app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --no-editable

# builder-dev
FROM builder AS builder-dev

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-editable

# dev
FROM base AS dev

COPY --from=builder-dev /app/.venv /app/.venv
COPY alembic ./alembic
COPY alembic.ini .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# prod
FROM base AS prod

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/app ./app
COPY alembic ./alembic
COPY alembic.ini .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
