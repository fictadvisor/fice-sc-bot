from aiogram.filters import CommandObject
from aiogram.types import Message

from bot.messages.errors import USER_NOT_FOUND, ONLY_FOR_TOPIC
from bot.messages.group import SET_RESPONSIBLE
from bot.repositories.topic import TopicFilter
from bot.repositories.uow import UnitOfWork
from bot.repositories.user import UserFilter


async def responsible(message: Message, command: CommandObject, uow: UnitOfWork):
    user = await uow.users.find_one(UserFilter(username=command.args))
    if not user:
        await message.reply(USER_NOT_FOUND)
        return

    if message.reply_to_message and message.reply_to_message.forum_topic_created:
        topic = await uow.topics.find_one(
            TopicFilter(group_id=message.chat.id, thread_id=message.reply_to_message.message_id))
        topic.responsible_id = user.id
        await message.reply(SET_RESPONSIBLE)
        return

    await message.reply(ONLY_FOR_TOPIC)
