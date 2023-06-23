from typing import Optional, Sequence

from pydantic import BaseModel
from sqlalchemy import select
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
            options: Optional[Sequence[ExecutableOption]] = None
    ) -> Sequence[Group]:
        query = select(self.__model__)

        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)
        if options is not None:
            query = query.options(*options)

        return (await self._session.scalars(query)).all()

    async def find_one(
            self,
            group_filter: GroupFilter,
            offset: Optional[int] = None,
            options: Optional[Sequence[ExecutableOption]] = None
    ) -> Optional[Group]:
        query = select(self.__model__).limit(1)

        if offset is not None:
            query = query.offset(offset)
        if options is not None:
            query = query.options(*options)

        return (await self._session.scalars(query)).first()
