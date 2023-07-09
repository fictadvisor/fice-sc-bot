from typing import Optional, Sequence

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.sql.base import ExecutableOption

from bot.models.message import Message
from bot.repositories.base import BaseRepository


class MessageFilter(BaseModel):
    chat_id: Optional[int] = None
    message_id: Optional[int] = None
    media_group_id: Optional[str] = None
    forward_from_chat_id: Optional[int] = None
    forward_from_message_id: Optional[int] = None


class MessageRepository(BaseRepository[Message]):
    __model__ = Message

    async def find(
            self,
            message_filter: MessageFilter,
            limit: Optional[int] = None,
            offset: Optional[int] = None,
            options: Optional[Sequence[ExecutableOption]] = None
    ) -> Sequence[Message]:
        query = select(self.__model__)

        if message_filter.chat_id is not None:
            query = query.filter_by(chat_id=message_filter.chat_id)
        if message_filter.message_id is not None:
            query = query.filter_by(message_id=message_filter.message_id)
        if message_filter.media_group_id is not None:
            query = query.filter_by(media_group_id=message_filter.media_group_id)
        if message_filter.forward_from_chat_id is not None:
            query = query.filter_by(forward_from_chat_id=message_filter.forward_from_chat_id)
        if message_filter.forward_from_message_id is not None:
            query = query.filter_by(forward_from_message_id=message_filter.forward_from_message_id)
        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)
        if options is not None:
            query = query.options(*options)

        return (await self._session.scalars(query)).all()

    async def find_one(
            self,
            message_filter: MessageFilter,
            offset: Optional[int] = None,
            options: Optional[Sequence[ExecutableOption]] = None
    ) -> Optional[Message]:
        query = select(self.__model__).limit(1)

        if message_filter.chat_id is not None:
            query = query.filter_by(chat_id=message_filter.chat_id)
        if message_filter.message_id is not None:
            query = query.filter_by(message_id=message_filter.message_id)
        if message_filter.forward_from_chat_id is not None:
            query = query.filter_by(forward_from_chat_id=message_filter.forward_from_chat_id)
        if message_filter.forward_from_message_id is not None:
            query = query.filter_by(forward_from_message_id=message_filter.forward_from_message_id)
        if offset is not None:
            query = query.offset(offset)
        if options is not None:
            query = query.options(*options)

        return (await self._session.scalars(query)).first()
