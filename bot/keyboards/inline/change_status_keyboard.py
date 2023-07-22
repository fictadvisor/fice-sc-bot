from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.keyboards.inline.types.change_status import ChangeStatus


async def get_change_status_keyboard(chat_id: int, message_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="Змінити статус",
                   callback_data=ChangeStatus(chat_id=chat_id, message_id=message_id))

    return builder.as_markup()
