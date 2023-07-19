from aiogram.types import Message
from sqlalchemy.orm import selectinload

from bot.messages.group import GROUPS_MEMBERS
from bot.models import Group
from bot.repositories.group import GroupFilter
from bot.repositories.uow import UnitOfWork


async def groups_members(message: Message, uow: UnitOfWork):
    groups = await uow.groups.find(GroupFilter(), options=[selectinload(Group.users)])

    await message.answer(await GROUPS_MEMBERS.render_async(groups=groups))
