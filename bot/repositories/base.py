from typing import Generic, TypeVar, Sequence, Optional, Type, Any

from sqlalchemy import select, update, delete, func, ColumnElement
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ExecutableOption

from bot.models import Base

T = TypeVar('T', bound=Base)


class BaseRepository(Generic[T]):
    __model__: Type[T]

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_count(self) -> Optional[int]:
        query = select(func.count()).select_from(self.__model__)
        return await self._session.scalar(query)

    async def create(self, model: T) -> T:
        self._session.add(model)
        return model

    async def get(
            self,
            limit: Optional[int] = None,
            offset: Optional[int] = None,
            options: Optional[Sequence[ExecutableOption]] = None,
            order: Optional[Sequence[ColumnElement]] = None
    ) -> Sequence[T]:
        query = select(self.__model__)

        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)
        if options is not None:
            query = query.options(*options)
        if order is not None:
            query = query.order_by(*order)

        return (await self._session.scalars(query)).all()

    async def get_by_id(
            self,
            model_id: int,
            options: Optional[Sequence[ExecutableOption]] = None
    ) -> Optional[T]:
        return await self._session.get(self.__model__, model_id, options=options)

    async def update(self, model_id: int, **kwargs: Any) -> None:
        query = update(self.__model__) \
            .where(self.__model__.id == model_id) \
            .values(**kwargs) \
            .execution_options(synchronize_session="evaluate")
        await self._session.execute(query)

    async def delete(self, model_id: int) -> None:
        query = delete(self.__model__).where(self.__model__.id == model_id)
        await self._session.execute(query)
