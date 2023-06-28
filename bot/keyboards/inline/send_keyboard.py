from typing import Sequence

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.keyboards.inline.types.send_message import SendMessage
from bot.models import Group


async def get_send_keyboard(groups: Sequence[Group], message_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for group in groups:
        builder.button(text=group.title, callback_data=SendMessage(chat_id=group.id, message_id=message_id))

    builder.adjust(1)

    return builder.as_markup()
