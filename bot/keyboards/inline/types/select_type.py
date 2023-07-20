from aiogram.filters.callback_data import CallbackData

from bot._types.message_types import MessageTypes


class SelectType(CallbackData, prefix="type"):
    type: MessageTypes
