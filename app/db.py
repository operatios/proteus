import datetime as dt
from collections.abc import AsyncIterator
from typing import Annotated

from sqlalchemy import DateTime, Identity, func
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Mapped, mapped_column

from app.settings import settings


class TimestampMixin:
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )


intpk = Annotated[int, mapped_column(Identity(always=True), primary_key=True)]

"""
More examples from SQLAlchemy docs:
timestamp = Annotated[
    datetime.datetime,
    mapped_column(nullable=False, server_default=func.CURRENT_TIMESTAMP()),
]
required_name = Annotated[str, mapped_column(String(30), nullable=False)]
"""


engine = create_async_engine(str(settings.DB_URL), echo=settings.SQL_ECHO)
sessionmaker = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_session() -> AsyncIterator[AsyncSession]:
    async with sessionmaker() as session:
        yield session
