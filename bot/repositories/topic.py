from typing import Optional, Sequence

from pydantic import BaseModel
from sqlalchemy import select, ColumnElement
from sqlalchemy.sql.base import ExecutableOption

from bot.models import Topic
from bot.repositories.base import BaseRepository


class TopicFilter(BaseModel):
    group_id: Optional[int] = None
    thread_id: Optional[int] = None
    responsible_id: Optional[int] = None
    title: Optional[str] = None


class TopicRepository(BaseRepository[Topic, TopicFilter]):
    __model__ = Topic

    async def get_all_by_filter_with_responsible(
            self,
            model_filter: TopicFilter,
            limit: Optional[int] = None,
            offset: Optional[int] = None,
            options: Optional[Sequence[ExecutableOption]] = None,
            order: Optional[Sequence[ColumnElement]] = None
    ) -> Sequence[Topic]:
        query = select(self.__model__)

        query = self._set_filter(query, model_filter, limit, offset, options, order)
        query = query.filter(~self.__model__.responsible_id.is_(None))

        return (await self._session.scalars(query)).all()
