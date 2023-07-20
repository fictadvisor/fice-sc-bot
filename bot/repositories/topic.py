from typing import Optional, Sequence

from pydantic import BaseModel
from sqlalchemy import select, ColumnElement
from sqlalchemy.sql.base import ExecutableOption

from bot.models import Topic
from bot.repositories.base import BaseRepository


class TopicFilter(BaseModel):
    group_id: Optional[int] = None
    thread_id: Optional[int] = None
    title: Optional[str] = None


class TopicRepository(BaseRepository[Topic]):
    __model__ = Topic

    async def find(
            self,
            topic_filter: TopicFilter,
            limit: Optional[int] = None,
            offset: Optional[int] = None,
            options: Optional[Sequence[ExecutableOption]] = None,
            order: Optional[Sequence[ColumnElement]] = None
    ) -> Sequence[Topic]:
        query = select(self.__model__)

        query = self._set_filter(query, topic_filter, limit, offset, options, order)

        return (await self._session.scalars(query)).all()

    async def find_one(
            self,
            topic_filter: TopicFilter,
            offset: Optional[int] = None,
            options: Optional[Sequence[ExecutableOption]] = None,
            order: Optional[Sequence[ColumnElement]] = None
    ) -> Optional[Topic]:
        query = select(self.__model__).limit(1)

        query = self._set_filter(query, topic_filter, 1, offset, options, order)

        return (await self._session.scalars(query)).first()
