from aiogram.filters.callback_data import CallbackData


class ChangeStatus(CallbackData, prefix="statusedit"):
    chat_id: int
    message_id: int
