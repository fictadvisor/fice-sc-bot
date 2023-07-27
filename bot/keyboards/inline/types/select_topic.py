from typing import Optional

from aiogram.filters.callback_data import CallbackData


class SelectTopic(CallbackData, prefix="topic"):
    chat_id: int
    thread_id: Optional[int] = None
