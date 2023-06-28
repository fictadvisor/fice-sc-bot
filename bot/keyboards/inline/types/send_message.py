from aiogram.filters.callback_data import CallbackData


class SendMessage(CallbackData, prefix="send_chat"):
    chat_id: int
    message_id: int
