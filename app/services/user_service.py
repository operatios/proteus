from fastapi.concurrency import run_in_threadpool
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import security
from app.models import User


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        res = await self.session.execute(stmt)

        return res.scalar_one_or_none()

    async def create(self, username: str, email: str, password: str) -> User:
        user = User(
            username=username,
            email=email,
            hashed_password=security.hash_password(password),
            is_active=True,
        )

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def authenticate_credentials(
        self, username: str, password: str
    ) -> User | None:
        user = await self.get_by_username(username)
        hash = user.hashed_password if user else security.DUMMY_HASH

        if await run_in_threadpool(
            security.verify_password, password=password, hash=hash
        ):
            return user
        return None
