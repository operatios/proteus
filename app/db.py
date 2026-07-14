from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# TODO
# https://pydantic.dev/docs/validation/latest/concepts/pydantic_settings/
DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_NAME = "postgres"

engine = create_async_engine(
    f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@db:5432/{DB_NAME}"
)
sessionmaker = async_sessionmaker()


async def get_session() -> AsyncIterator[AsyncSession]:
    async with sessionmaker() as session:
        yield session
