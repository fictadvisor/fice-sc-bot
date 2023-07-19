from aiogram.types import Message

from bot.models import Group
from bot.repositories.uow import UnitOfWork


async def rename_group(message: Message, uow: UnitOfWork) -> None:
    group = await uow.groups.get_by_id(message.chat.id)

    if group is None:
        group = Group(
            id=message.chat.id,
            title=message.new_chat_title
        )
        await uow.groups.create(group)
    else:
        group.title = message.new_chat_title
