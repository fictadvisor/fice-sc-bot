from typing import Optional

from aiogram import Bot
from aiogram.types import Message

from bot._types import Album
from bot.models import Message as MessageModel
from bot.repositories.uow import UnitOfWork
from bot.services.message import MessageService


async def reply_message(message: Message, bot: Bot, uow: UnitOfWork, main_message: MessageModel,
                        album: Optional[Album] = None):
    message_service = MessageService(bot, uow)
    await message_service.reply_message(message, main_message, album)
