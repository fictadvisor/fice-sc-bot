from aiogram.types import Message
from sqlalchemy.orm import selectinload

from bot.messages.group import GROUP_MEMBERS
from bot.models import Group
from bot.repositories.uow import UnitOfWork


async def group_members(message: Message, uow: UnitOfWork):
    group = await uow.groups.get_by_id(message.chat.id, [selectinload(Group.users)])

    await message.answer(await GROUP_MEMBERS.render_async(group=group))
