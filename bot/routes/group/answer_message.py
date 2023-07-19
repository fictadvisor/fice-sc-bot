from typing import Optional

from aiogram import Bot
from aiogram.types import Message

from bot._types import Album
from bot.repositories.uow import UnitOfWork
from bot.services.message import MessageService


async def answer_message(message: Message, bot: Bot, uow: UnitOfWork, album: Optional[Album] = None) -> None:
    message_service = MessageService(bot, uow)
    await message_service.answer_message(message, album)
