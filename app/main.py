from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pydantic import BaseModel


class FooSchema(BaseModel):
    name: str
    age: int


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    yield


app = FastAPI(lifespan=lifespan)
# TODO:
# v1/v2
# app.include_router()


@app.get("/")
async def root() -> str:
    return "Hello!"


@app.get("/foo")
async def get_foo(foo: bool) -> dict[Any, Any]:
    return {"value": foo}


@app.get("/teleport")
async def get_teleport() -> RedirectResponse:
    return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
