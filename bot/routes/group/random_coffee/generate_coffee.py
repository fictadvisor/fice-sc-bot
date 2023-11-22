import itertools
import math
from typing import List

from aiogram.types import Message
from sqlalchemy.orm import selectinload

from bot.messages.group import RANDOM_COFFEE
from bot.models import Group, RandomCoffee, RandomCoffeePair
from bot.repositories.random_coffee_pair import RandomCoffeePairFilter
from bot.repositories.uow import UnitOfWork


async def generate_coffee(message: Message, uow: UnitOfWork):
    group = await uow.groups.get_by_id(message.chat.id, [selectinload(Group.users)])

    random_coffee = RandomCoffee(group_id=group.id)
    await uow.random_coffee.create(random_coffee)

    combinations = itertools.combinations(group.users, 2)
    count = 0
    exclude: List[int] = []
    for first, second in combinations:
        if count == math.ceil(len(group.users) / 2):
            break
        if first.id < second.id:
            first, second = second, first
        if first.id in exclude or second.id in exclude:
            continue
        if await uow.random_coffee_pairs.find_one(RandomCoffeePairFilter(first_id=first.id, second_id=second.id)):
            continue

        pair = RandomCoffeePair(first=first, second=second, group_id=group.id)
        random_coffee.pairs.append(pair)
        count += 1
        exclude.extend((first.id, second.id))

    if len(random_coffee.pairs) == 0:
        await message.answer("Всі пари вже були")
    else:
        await message.answer(await RANDOM_COFFEE.render_async(pairs=random_coffee.pairs))
