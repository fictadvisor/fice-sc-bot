from aiogram.types import ChatMemberUpdated
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models import Group
from bot.repositories.group import GroupRepository


async def invite_bot(event: ChatMemberUpdated, session: AsyncSession):
    group_repository = GroupRepository(session)
    group = await group_repository.get_by_id(event.chat.id)
    if group is None:
        group = Group(
            id=event.chat.id,
            title=event.chat.title
        )
        await group_repository.create(group)
