from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from bot.models import User, Group
from bot.repositories.group import GroupRepository
from bot.repositories.user import UserRepository


async def messages(message: Message, session: AsyncSession):
    group_repository = GroupRepository(session)
    group = await group_repository.get_by_id(message.chat.id, [selectinload(Group.users)])
    if group is None:
        group = Group(
            id=message.chat.id,
            title=message.chat.title
        )
        await group_repository.create(group)

    user_repository = UserRepository(session)
    user = await user_repository.get_by_id(message.from_user.id, [selectinload(User.groups)])
    if user is None:
        user = User(
            id=message.from_user.id,
            username=f"@{message.from_user.username}"
            if message.from_user.username
            else message.from_user.full_name
        )
        await user_repository.create(user)
    elif user.username != message.from_user.username:
        user.username = f"@{message.from_user.username}" \
            if message.from_user.username \
            else message.from_user.full_name

    group.users.append(user)
