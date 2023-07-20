from aiogram.types import Message

from bot.keyboards.inline.type_keyboard import get_type_keyboard
from bot.messages.group import SELECT_TYPE
from bot.models import Message as MessageModel
from bot.repositories.message import MessageFilter
from bot.repositories.uow import UnitOfWork


async def send(message: Message, uow: UnitOfWork) -> None:
    await message.delete()

    if not message.reply_to_message.media_group_id:
        if not await uow.messages.check_exists(
                MessageFilter(chat_id=message.chat.id, message_id=message.reply_to_message.message_id)):
            message_model = MessageModel(
                chat_id=message.chat.id,
                message_id=message.reply_to_message.message_id,
                from_user_id=message.reply_to_message.from_user.id,
                html_text=message.reply_to_message.html_text
            )
            await uow.messages.create(message_model)

    await message.reply_to_message.reply(
        text=SELECT_TYPE,
        reply_markup=await get_type_keyboard()
    )
