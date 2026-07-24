from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base

# TODO: created_at field


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)  # TODO: maybe use CITEXT
    hashed_password: Mapped[str]
    is_active: Mapped[bool]
