from aiogram.types import ChatMemberUpdated
from sqlalchemy.orm import selectinload

from bot.models import User
from bot.repositories.uow import UnitOfWork


async def kick_member(event: ChatMemberUpdated, uow: UnitOfWork):
    user = await uow.users.get_by_id(event.new_chat_member.user.id, [selectinload(User.groups)])
    if user is not None:
        await uow.users.delete(user.id)
