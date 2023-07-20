from typing import Sequence

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.keyboards.inline.types.select_group import SelectGroup
from bot.models import Group


async def get_group_keyboard(groups: Sequence[Group]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for group in groups:
        builder.button(text=group.title, callback_data=SelectGroup(chat_id=group.id))

    builder.adjust(1)

    return builder.as_markup()
