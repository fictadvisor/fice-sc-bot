from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from bot.models import Base


class Topic(Base):
    __tablename__ = "topics"

    group_id: Mapped[BigInteger] = mapped_column(ForeignKey("groups.id"))
    thread_id: Mapped[int] = mapped_column(BigInteger)
    title: Mapped[str]
