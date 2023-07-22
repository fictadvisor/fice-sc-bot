from aiogram.filters.callback_data import CallbackData

from bot._types.status import Status


class SelectStatus(CallbackData, prefix="status"):
    chat_id: int
    message_id: int
    status: Status
