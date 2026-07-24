from sqlalchemy import CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class SubscriptionGroup(Base):
    __tablename__ = "subscription_group"
    __table_args__ = CheckConstraint("update_interval > 30")

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    urls: Mapped[list[str]]
    update_interval: Mapped[int] = mapped_column()
