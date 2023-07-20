from aiogram.filters.callback_data import CallbackData


class SelectGroup(CallbackData, prefix="send_chat"):
    chat_id: int
