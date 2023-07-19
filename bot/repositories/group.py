from typing import Optional, Sequence

from pydantic import BaseModel
from sqlalchemy import select, ColumnElement
from sqlalchemy.sql.base import ExecutableOption

from bot.models import Group
from bot.repositories.base import BaseRepository


class GroupFilter(BaseModel):
    title: Optional[str] = None


class GroupRepository(BaseRepository[Group]):
    __model__ = Group

    async def find(
            self,
            group_filter: GroupFilter,
            limit: Optional[int] = None,
            offset: Optional[int] = None,
            options: Optional[Sequence[ExecutableOption]] = None,
            order: Optional[Sequence[ColumnElement]] = None
    ) -> Sequence[Group]:
        query = select(self.__model__)

        query = self._set_filter(query, group_filter, limit, offset, options, order)

        return (await self._session.scalars(query)).all()

    async def find_one(
            self,
            group_filter: GroupFilter,
            offset: Optional[int] = None,
            options: Optional[Sequence[ExecutableOption]] = None,
            order: Optional[Sequence[ColumnElement]] = None
    ) -> Optional[Group]:
        query = select(self.__model__).limit(1)

        query = self._set_filter(query, group_filter, 1, offset, options, order)

        return (await self._session.scalars(query)).first()
