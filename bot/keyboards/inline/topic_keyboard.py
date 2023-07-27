from typing import List

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.keyboards.inline.types.select_topic import SelectTopic
from bot.models import Topic


async def get_topic_keyboard(chat_id: int, topics: List[Topic]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for topic in topics:
        builder.button(text=topic.title, callback_data=SelectTopic(chat_id=chat_id, thread_id=topic.thread_id))
    builder.button(text="Інше", callback_data=SelectTopic(chat_id=chat_id))

    if len(topics) <= 8:
        builder.adjust(1)
    else:
        builder.adjust(2)

    return builder.as_markup()
