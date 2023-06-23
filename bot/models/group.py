from typing import List, TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from bot.models import Base

if TYPE_CHECKING:
    from bot.models.user import User


class Group(Base):
    __tablename__ = "groups"

    title: Mapped[str]

    users: Mapped[List["User"]] = relationship(
        secondary="usergrouplink", back_populates="groups"
    )
