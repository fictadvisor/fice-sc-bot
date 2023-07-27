from typing import Optional

from pydantic import BaseModel

from bot.models.message import Message
from bot.repositories.base import BaseRepository


class MessageFilter(BaseModel):
    chat_id: Optional[int] = None
    message_id: Optional[int] = None
    media_group_id: Optional[str] = None
    forward_from_chat_id: Optional[int] = None
    forward_from_message_id: Optional[int] = None


class MessageRepository(BaseRepository[Message, MessageFilter]):
    __model__ = Message
