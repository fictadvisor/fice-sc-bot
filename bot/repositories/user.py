from typing import Optional, Sequence

from pydantic import BaseModel
from sqlalchemy import select, ColumnElement
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
            options: Optional[Sequence[ExecutableOption]] = None,
            order: Optional[Sequence[ColumnElement]] = None
    ) -> Sequence[User]:
        query = select(self.__model__)

        query = self._set_filter(query, user_filter, limit, offset, options, order)

        return (await self._session.scalars(query)).all()

    async def find_one(
            self,
            user_filter: UserFilter,
            offset: Optional[int] = None,
            options: Optional[Sequence[ExecutableOption]] = None,
            order: Optional[Sequence[ColumnElement]] = None
    ) -> Optional[User]:
        query = select(self.__model__).limit(1)

        query = self._set_filter(query, user_filter, 1, offset, options, order)

        return (await self._session.scalars(query)).first()
