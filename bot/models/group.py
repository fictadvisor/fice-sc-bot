from typing import List, TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from bot.models import Base
from bot.models.topic import Topic

if TYPE_CHECKING:
    from bot.models.user import User


class Group(Base):
    __tablename__ = "groups"

    title: Mapped[str]
    topics: Mapped[Topic] = relationship()

    users: Mapped[List["User"]] = relationship(
        secondary="usergrouplink", back_populates="groups"
    )
