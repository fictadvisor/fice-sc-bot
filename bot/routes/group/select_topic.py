from aiogram import Bot
from aiogram.types import CallbackQuery

from bot.keyboards.inline.types.select_topic import SelectTopic
from bot.messages.group import SENT
from bot.repositories.uow import UnitOfWork
from bot.services.message import MessageService


async def select_topic(callback: CallbackQuery, callback_data: SelectTopic, bot: Bot, uow: UnitOfWork) -> None:
    message_service = MessageService(bot, uow)
    await message_service.send_to_group(
        callback_data.chat_id,
        callback.message.chat.title,
        callback.message.reply_to_message.message_id,
        callback.message.chat.id,
        callback_data.thread_id
    )

    await callback.message.edit_text(await SENT.render_async(title=message_service.get_chat_title()))
