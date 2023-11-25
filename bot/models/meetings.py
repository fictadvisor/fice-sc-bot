from sqlalchemy.sql import func

from sqlalchemy import BigInteger, DateTime, Interval
from sqlalchemy.orm import Mapped, mapped_column

from bot.models import Base

class Meetings(Base):
    __tablename__ = "meetings"

    meeting_id: Mapped[int] = mapped_column(BigInteger)
    title: Mapped(str)
    start_time: Mapped(DateTime)= mapped_column(func.now())
    duration: Mapped(Interval)