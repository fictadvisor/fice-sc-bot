from sqlalchemy import ForeignKey, BigInteger, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.models import Base, User


class RandomCoffeePair(Base):
    __tablename__ = "random_coffee_pairs"

    random_coffee_id: Mapped[int] = mapped_column(ForeignKey("random_coffee.id", ondelete="CASCADE"))
    group_id: Mapped[BigInteger] = mapped_column(ForeignKey("groups.id", ondelete="CASCADE"))
    first_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    first: Mapped[User] = relationship(foreign_keys=[first_id])
    second_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    second: Mapped[User] = relationship(foreign_keys=[second_id])

    __table_args__ = (
        UniqueConstraint('group_id', 'first_id', 'second_id'),
    )
