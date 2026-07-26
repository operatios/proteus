from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import redis.asyncio as redis
from fastapi import FastAPI
from pydantic import BaseModel


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    yield


app = FastAPI(lifespan=lifespan)
r = redis.Redis(host="redis", port=6379, decode_responses=True)
# TODO:
# v1/v2
# app.include_router()


@app.get("/health")
def get_health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/")
async def get_root() -> str:
    return "Hello, friend!"


@app.get("/redis")
async def get_redis(key: str, value: str | None = None) -> bool | str | bytes | None:
    if value is not None:
        return await r.set(key, value)

    return await r.get(key)
