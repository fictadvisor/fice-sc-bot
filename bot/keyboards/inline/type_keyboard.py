from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot._types.message_types import MessageTypes
from bot.keyboards.inline.types.select_type import SelectType


async def get_type_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for i in MessageTypes:
        builder.button(text=i, callback_data=SelectType(type=MessageTypes(i)))
    builder.adjust(1)

    return builder.as_markup()
