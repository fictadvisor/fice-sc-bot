from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession

from bot.repositories.group import GroupRepository
from bot.repositories.message import MessageRepository
from bot.repositories.random_coffee import RandomCoffeeRepository
from bot.repositories.random_coffee_pair import RandomCoffeePairRepository
from bot.repositories.topic import TopicRepository
from bot.repositories.user import UserRepository


class UnitOfWork:
    _session: AsyncSession

    users: UserRepository
    groups: GroupRepository
    messages: MessageRepository
    topics: TopicRepository
    random_coffee: RandomCoffeeRepository
    random_coffee_pairs: RandomCoffeePairRepository

    def __init__(self, session: AsyncSession):
        self._session = session

    async def __aenter__(self) -> Self:
        self.users = UserRepository(self._session)
        self.groups = GroupRepository(self._session)
        self.messages = MessageRepository(self._session)
        self.topics = TopicRepository(self._session)
        self.random_coffee = RandomCoffeeRepository(self._session)
        self.random_coffee_pairs = RandomCoffeePairRepository(self._session)

        return self

    async def __aexit__(self, *args):
        ...

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()

    async def flush(self):
        await self._session.flush()

