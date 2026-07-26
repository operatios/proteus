# base
FROM python:3.14-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 8000


# builder
FROM base AS builder

COPY --from=ghcr.io/astral-sh/uv:0.11.32 /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

COPY README.md app ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

# builder-dev
FROM builder AS builder-dev

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked


# dev
FROM base AS dev

COPY --from=builder-dev /app/.venv /app/.venv

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]


# prod
FROM base AS prod

COPY app ./app
COPY --from=builder /app/.venv /app/.venv

# deduplicate cmd by setting args
# create unpriviliged user
# copy alembic
# healthcheck

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
