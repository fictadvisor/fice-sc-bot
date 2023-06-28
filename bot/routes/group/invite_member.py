from aiogram.types import ChatMemberUpdated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from bot.models import Group, User
from bot.repositories.group import GroupRepository
from bot.repositories.user import UserRepository


async def invite_member(event: ChatMemberUpdated, session: AsyncSession):
    group_repository = GroupRepository(session)
    group = await group_repository.get_by_id(event.chat.id, [selectinload(Group.users)])
    if group is None:
        group = Group(
            id=event.chat.id,
            title=event.chat.title
        )
        await group_repository.create(group)

    user_repository = UserRepository(session)
    user = await user_repository.get_by_id(event.new_chat_member.user.id, [selectinload(User.groups)])
    if user is None:
        user = User(
            id=event.new_chat_member.user.id,
            username=f"@{event.new_chat_member.user.username}"
            if event.new_chat_member.user.username
            else event.new_chat_member.user.mention_html()
        )
        await user_repository.create(user)

    group.users.append(user)
