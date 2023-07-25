from typing import Optional, TYPE_CHECKING

from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.models import Base

if TYPE_CHECKING:
    from bot.models import User


class Topic(Base):
    __tablename__ = "topics"

    group_id: Mapped[BigInteger] = mapped_column(ForeignKey("groups.id", ondelete="CASCADE"))
    thread_id: Mapped[int] = mapped_column(BigInteger)
    responsible_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    responsible: Mapped[Optional["User"]] = relationship()
    title: Mapped[str]
