from typing import List, TYPE_CHECKING

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.models import Base

if TYPE_CHECKING:
    from bot.models.group import Group


class User(Base):
    __tablename__ = "users"

    username: Mapped[str]

    groups: Mapped[List["Group"]] = relationship(
        secondary="usergrouplink", back_populates="users"
    )
