from typing import Optional, Sequence

from pydantic import BaseModel
from sqlalchemy import select, ColumnElement
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
            options: Optional[Sequence[ExecutableOption]] = None,
            order: Optional[Sequence[ColumnElement]] = None
    ) -> Sequence[Message]:
        query = select(self.__model__)

        query = self._set_filter(query, message_filter, limit, offset, options, order)

        return (await self._session.scalars(query)).all()

    async def find_one(
            self,
            message_filter: MessageFilter,
            offset: Optional[int] = None,
            options: Optional[Sequence[ExecutableOption]] = None,
            order: Optional[Sequence[ColumnElement]] = None
    ) -> Optional[Message]:
        query = select(self.__model__).limit(1)

        query = self._set_filter(query, message_filter, 1, offset, options, order)

        return (await self._session.scalars(query)).first()
