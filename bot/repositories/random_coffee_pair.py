from typing import Optional

from pydantic import BaseModel

from bot.models import RandomCoffeePair
from bot.repositories.base import BaseRepository


class RandomCoffeePairFilter(BaseModel):
    random_coffee_id: Optional[int] = None
    group_id: Optional[int] = None
    first_id: Optional[int] = None
    second_id: Optional[int] = None


class RandomCoffeePairRepository(BaseRepository[RandomCoffeePair, RandomCoffeePairFilter]):
    __model__ = RandomCoffeePair
