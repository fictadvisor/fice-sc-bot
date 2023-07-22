from aiogram.types import CallbackQuery

from bot._types.message_types import MessageTypes
from bot._types.status import Status
from bot.keyboards.inline.group_keyboard import get_group_keyboard
from bot.keyboards.inline.types.select_type import SelectType
from bot.messages.group import SELECT_GROUP
from bot.repositories.message import MessageFilter
from bot.repositories.uow import UnitOfWork


async def select_type(callback: CallbackQuery, callback_data: SelectType, uow: UnitOfWork) -> None:
    message = await uow.messages.find_one(
        MessageFilter(chat_id=callback.message.chat.id, message_id=callback.message.reply_to_message.message_id))
    message.type = callback_data.type
    if callback_data.type == MessageTypes.TASK:
        message.status = Status.NOT_STARTED

    groups = await uow.groups.get()
    await callback.message.edit_text(
        text=SELECT_GROUP,
        reply_markup=await get_group_keyboard(
            list(filter(lambda group: group.id != callback.message.chat.id, groups))
        ))
