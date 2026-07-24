from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.settings import settings


class Base(DeclarativeBase):
    pass


# TODO
# https://pydantic.dev/docs/validation/latest/concepts/pydantic_settings/
DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_NAME = "postgres"

print(settings.db_url)

engine = create_async_engine(
    url=str(settings.db_url),
    echo=True,
)
sessionmaker = async_sessionmaker()


async def get_session() -> AsyncIterator[AsyncSession]:
    # TODO: try / except / finally rollback
    async with sessionmaker() as session:
        yield session
