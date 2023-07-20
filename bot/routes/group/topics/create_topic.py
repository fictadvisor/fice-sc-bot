from aiogram.types import Message

from bot.models import Topic
from bot.repositories.uow import UnitOfWork


async def create_topic(message: Message, uow: UnitOfWork):
    topic = Topic(
        group_id=message.chat.id,
        thread_id=message.message_id,
        title=message.forum_topic_created.name
    )
    await uow.topics.create(topic)
