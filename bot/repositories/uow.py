from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession

from bot.repositories.group import GroupRepository
from bot.repositories.message import MessageRepository
from bot.repositories.user import UserRepository


class UnitOfWork:
    _session: AsyncSession

    users: UserRepository
    groups: GroupRepository
    messages: MessageRepository

    def __init__(self, session: AsyncSession):
        self._session = session

    async def __aenter__(self) -> Self:
        self.users = UserRepository(self._session)
        self.groups = GroupRepository(self._session)
        self.messages = MessageRepository(self._session)

        return self

    async def __aexit__(self, *args):
        ...

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()
