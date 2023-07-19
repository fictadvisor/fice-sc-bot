from aiogram.types import ChatMemberUpdated
from sqlalchemy.orm import selectinload

from bot.models import Group, User
from bot.repositories.uow import UnitOfWork


async def invite_member(event: ChatMemberUpdated, uow: UnitOfWork):
    group = await uow.groups.get_by_id(event.chat.id, [selectinload(Group.users)])
    if group is None:
        group = Group(
            id=event.chat.id,
            title=event.chat.title
        )
        await uow.groups.create(group)

    user = await uow.groups.get_by_id(event.new_chat_member.user.id, [selectinload(User.groups)])
    if user is None:
        user = User(
            id=event.new_chat_member.user.id,
            username=f"@{event.new_chat_member.user.username}"
            if event.new_chat_member.user.username
            else event.new_chat_member.user.full_name
        )
        await uow.groups.create(user)

    group.users.append(user)
