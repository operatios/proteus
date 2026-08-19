from sqlalchemy.orm import Mapped, mapped_column

from app.db import TimestampMixin, intpk
from app.models import Base


class User(Base, TimestampMixin):
    __tablename__ = "user"

    id: Mapped[intpk]

    username: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str]

    is_active: Mapped[bool]
