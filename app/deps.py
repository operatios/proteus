from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.services.user_service import UserService

SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def get_user_service(session: SessionDep) -> UserService:
    return UserService(session)
