from aiogram.types import Message
from sqlalchemy import desc
from sqlalchemy.orm import selectinload

from bot.messages.group import MY_COFFEE
from bot.models import RandomCoffeePair
from bot.repositories.random_coffee_pair import RandomCoffeePairFilter
from bot.repositories.uow import UnitOfWork


async def my_coffee(message: Message, uow: UnitOfWork):
    pair = max(
        await uow.random_coffee_pairs.find_one(
            RandomCoffeePairFilter(first_id=message.from_user.id, group_id=message.chat.id),
            order=[desc(RandomCoffeePair.id)],
            options=[selectinload(RandomCoffeePair.first), selectinload(RandomCoffeePair.second)]),
        await uow.random_coffee_pairs.find_one(
            RandomCoffeePairFilter(second_id=message.from_user.id, group_id=message.chat.id),
            order=[desc(RandomCoffeePair.id)],
            options=[selectinload(RandomCoffeePair.first), selectinload(RandomCoffeePair.second)]),
        key=lambda x: x.id if x else -1
    )
    if not pair:
        await message.answer("В тебе немає пари")
        return
    await message.answer(await MY_COFFEE.render_async(pair=pair))
