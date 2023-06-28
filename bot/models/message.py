from typing import Optional

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from bot.models import Base


class Message(Base):
    __tablename__ = "messages"

    chat_id: Mapped[int] = mapped_column(BigInteger)
    message_id: Mapped[int] = mapped_column(BigInteger)
    from_user_id: Mapped[int] = mapped_column(BigInteger)
    text: Mapped[Optional[str]]
    forward_from_chat_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    forward_from_message_id: Mapped[Optional[int]] = mapped_column(BigInteger)
