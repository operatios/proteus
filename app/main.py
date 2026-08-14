import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.routers import auth, base

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    yield


# TODO: @app.exception_handler
# https://fastapi.tiangolo.com/tutorial/metadata/
app = FastAPI(lifespan=lifespan)


app.include_router(base.router)
app.include_router(auth.router, prefix="/auth")
