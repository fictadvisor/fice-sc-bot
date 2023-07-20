from aiogram.types import Message

from bot.repositories.topic import TopicFilter
from bot.repositories.uow import UnitOfWork


async def close_topic(message: Message, uow: UnitOfWork):
    topic = await uow.topics.find_one(
        TopicFilter(group_id=message.chat.id, thread_id=message.reply_to_message.message_id))
    if topic:
        await uow.topics.delete(topic.id)
