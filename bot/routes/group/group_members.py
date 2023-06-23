from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from bot.messages.group import GROUP_MEMBERS
from bot.models import Group
from bot.repositories.group import GroupRepository


async def group_members(message: Message, session: AsyncSession):
    group_repository = GroupRepository(session)
    group = await group_repository.get_by_id(message.chat.id, [selectinload(Group.users)])

    await message.answer(await GROUP_MEMBERS.render_async(group=group))
