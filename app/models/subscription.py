from sqlalchemy import CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db import intpk
from app.models import Base


class SubscriptionGroup(Base):
    __tablename__ = "subscription_group"
    __table_args__ = CheckConstraint("update_interval > 1800")

    id: Mapped[intpk]
    name: Mapped[str]
    update_interval: Mapped[int]
