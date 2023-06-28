from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models import Group
from bot.repositories.group import GroupRepository


async def rename_group(message: Message, session: AsyncSession) -> None:
    group_repository = GroupRepository(session)
    group = await group_repository.get_by_id(message.chat.id)

    if group is None:
        group = Group(
            id=message.chat.id,
            title=message.new_chat_title
        )
        await group_repository.create(group)
    else:
        group.title = message.new_chat_title
