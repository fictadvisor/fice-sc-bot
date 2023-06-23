from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from bot.messages.group import ALL_MEMBERS
from bot.models import Group
from bot.repositories.group import GroupRepository, GroupFilter


async def all_members(message: Message, session: AsyncSession):
    group_repository = GroupRepository(session)
    groups = await group_repository.find(GroupFilter(), options=[selectinload(Group.users)])

    await message.answer(await ALL_MEMBERS.render_async(groups=groups))

