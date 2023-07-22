from typing import Optional

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from bot._types import MediaTypes
from bot._types.message_types import MessageTypes
from bot._types.status import Status
from bot.models import Base


class Message(Base):
    __tablename__ = "messages"

    chat_id: Mapped[int] = mapped_column(BigInteger)
    message_id: Mapped[int] = mapped_column(BigInteger)
    media_group_id: Mapped[Optional[str]]
    file_id: Mapped[Optional[str]]
    media_type: Mapped[Optional[MediaTypes]]
    type: Mapped[Optional[MessageTypes]]
    status: Mapped[Optional[Status]]
    from_user_id: Mapped[int] = mapped_column(BigInteger)
    html_text: Mapped[Optional[str]]
    forward_from_chat_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    forward_from_message_id: Mapped[Optional[int]] = mapped_column(BigInteger)
