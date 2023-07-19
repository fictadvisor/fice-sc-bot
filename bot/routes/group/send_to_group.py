from aiogram import Bot
from aiogram.types import CallbackQuery

from bot.keyboards.inline.types.send_message import SendMessage
from bot.messages.group import SENT
from bot.repositories.uow import UnitOfWork
from bot.services.message import MessageService


async def send_to_group(callback: CallbackQuery, callback_data: SendMessage, bot: Bot, uow: UnitOfWork) -> None:
    message_service = MessageService(bot, uow)
    await message_service.send_to_group(callback_data.chat_id, callback.message.chat.title, callback_data.message_id,
                                        callback.message.chat.id)

    await callback.message.edit_text(await SENT.render_async(title=message_service.get_chat_title()))
