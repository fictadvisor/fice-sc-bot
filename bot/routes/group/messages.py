from aiogram.types import Message
from sqlalchemy.orm import selectinload

from bot.models import User, Group
from bot.repositories.uow import UnitOfWork


async def messages(message: Message, uow: UnitOfWork):
    group = await uow.groups.get_by_id(message.chat.id, [selectinload(Group.users)])
    if group is None:
        group = Group(
            id=message.chat.id,
            title=message.chat.title
        )
        await uow.groups.create(group)

    user = await uow.users.get_by_id(message.from_user.id, [selectinload(User.groups)])
    if user is None:
        user = User(
            id=message.from_user.id,
            username=f"@{message.from_user.username}"
            if message.from_user.username
            else message.from_user.full_name
        )
        await uow.users.create(user)
    elif user.username != message.from_user.username:
        user.username = f"@{message.from_user.username}" \
            if message.from_user.username \
            else message.from_user.full_name

    group.users.append(user)
