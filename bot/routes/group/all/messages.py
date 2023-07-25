from aiogram.types import Message
from sqlalchemy.orm import selectinload

from bot.models import User, Group
from bot.repositories.topic import TopicFilter
from bot.repositories.uow import UnitOfWork
from bot.routes.group.topics import create_topic


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

    if message.reply_to_message and message.reply_to_message.forum_topic_created:
        if not await uow.topics.check_exists(
                TopicFilter(group_id=message.chat.id, thread_id=message.reply_to_message.message_id)):
            await create_topic(message.reply_to_message, uow)
