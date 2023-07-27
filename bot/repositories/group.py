from typing import Optional

from pydantic import BaseModel

from bot.models import Group
from bot.repositories.base import BaseRepository


class GroupFilter(BaseModel):
    title: Optional[str] = None


class GroupRepository(BaseRepository[Group, GroupFilter]):
    __model__ = Group
