from aiogram.types import ChatMemberUpdated

from bot.models import Group
from bot.repositories.uow import UnitOfWork


async def invite_bot(event: ChatMemberUpdated, uow: UnitOfWork):
    group = await uow.groups.get_by_id(event.chat.id)
    if group is None:
        group = Group(
            id=event.chat.id,
            title=event.chat.title
        )
        await uow.groups.create(group)
