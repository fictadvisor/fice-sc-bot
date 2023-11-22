from typing import Optional

from pydantic import BaseModel

from bot.models import RandomCoffee
from bot.repositories.base import BaseRepository


class RandomCoffeeFilter(BaseModel):
    group_id: Optional[int] = None


class RandomCoffeeRepository(BaseRepository[RandomCoffee, RandomCoffeeFilter]):
    __model__ = RandomCoffee
