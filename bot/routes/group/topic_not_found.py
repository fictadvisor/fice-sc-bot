from aiogram.types import ErrorEvent

from bot.keyboards.inline.types.select_topic import SelectTopic
from bot.messages.errors import TOPIC_NOT_FOUND
from bot.repositories.topic import TopicFilter
from bot.repositories.uow import UnitOfWork


async def topic_not_found(exception: ErrorEvent, uow: UnitOfWork):
    callback_data = SelectTopic.unpack(exception.update.callback_query.data)
    topic = await uow.topics.find_one(TopicFilter(
        group_id=callback_data.chat_id,
        thread_id=callback_data.thread_id
    ))

    await exception.update.callback_query.message.edit_text(await TOPIC_NOT_FOUND.render_async(title=topic.title))
    await uow.topics.delete(topic.id)
