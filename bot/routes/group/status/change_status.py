from aiogram.types import CallbackQuery

from bot.keyboards.inline.status_keyboard import get_status_keyboard
from bot.keyboards.inline.types.change_status import ChangeStatus


async def change_status(callback: CallbackQuery, callback_data: ChangeStatus):
    await callback.message.edit_reply_markup(
        reply_markup=await get_status_keyboard(callback_data.chat_id, callback_data.message_id))
