from typing import Optional, Sequence

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.sql.base import ExecutableOption

from bot.models import User
from bot.repositories.base import BaseRepository


class UserFilter(BaseModel):
    username: Optional[str] = None


class UserRepository(BaseRepository[User]):
    __model__ = User

    async def find(
            self,
            user_filter: UserFilter,
            limit: Optional[int] = None,
            offset: Optional[int] = None,
            options: Optional[Sequence[ExecutableOption]] = None
    ) -> Sequence[User]:
        query = select(self.__model__)

        if user_filter.username is not None:
            query = query.filter_by(username=user_filter.username)
        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)
        if options is not None:
            query = query.options(*options)

        return (await self._session.scalars(query)).all()

    async def find_one(
            self,
            user_filter: UserFilter,
            offset: Optional[int] = None,
            options: Optional[Sequence[ExecutableOption]] = None
    ) -> Optional[User]:
        query = select(self.__model__).limit(1)

        if user_filter.username is not None:
            query = query.filter_by(username=user_filter.username)
        if offset is not None:
            query = query.offset(offset)
        if options is not None:
            query = query.options(*options)

        return (await self._session.scalars(query)).first()
