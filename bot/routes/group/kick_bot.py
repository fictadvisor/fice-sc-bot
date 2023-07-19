from aiogram.types import ChatMemberUpdated

from bot.repositories.uow import UnitOfWork


async def kick_bot(event: ChatMemberUpdated, uow: UnitOfWork):
    group = await uow.groups.get_by_id(event.chat.id)
    if group is not None:
        await uow.groups.delete(group.id)
