from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot._types.status import Status
from bot.keyboards.inline.types.select_status import SelectStatus


async def get_status_keyboard(chat_id: int, message_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for i in Status:
        builder.button(text=i, callback_data=SelectStatus(chat_id=chat_id, message_id=message_id, status=Status(i)))
    builder.adjust(1)

    return builder.as_markup()
