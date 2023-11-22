from typing import List

from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.models import Base
from bot.models.random_coffee_pair import RandomCoffeePair


class RandomCoffee(Base):
    __tablename__ = "random_coffee"

    group_id: Mapped[BigInteger] = mapped_column(ForeignKey("groups.id", ondelete="CASCADE"))
    pairs: Mapped[List[RandomCoffeePair]] = relationship()
