from aiogram.types import ChatMemberUpdated
from sqlalchemy.ext.asyncio import AsyncSession

from bot.repositories.group import GroupRepository


async def kick_bot(event: ChatMemberUpdated, session: AsyncSession):
    group_repository = GroupRepository(session)
    group = await group_repository.get_by_id(event.chat.id)
    if group is not None:
        await group_repository.delete(group.id)
