from typing import Optional

from pydantic import BaseModel

from bot.models import User
from bot.repositories.base import BaseRepository


class UserFilter(BaseModel):
    username: Optional[str] = None


class UserRepository(BaseRepository[User, UserFilter]):
    __model__ = User
