from aiogram.filters.callback_data import CallbackData


class SelectTopic(CallbackData, prefix="topic"):
    chat_id: int
    thread_id: int
