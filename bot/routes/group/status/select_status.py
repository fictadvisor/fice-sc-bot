from aiogram import Bot
from aiogram.types import CallbackQuery

from bot.keyboards.inline.types.select_status import SelectStatus
from bot.repositories.uow import UnitOfWork
from bot.services.message import MessageService


async def select_status(callback: CallbackQuery, callback_data: SelectStatus, bot: Bot, uow: UnitOfWork):
    message_service = MessageService(bot, uow)
    await message_service.change_status(callback.message, callback_data)
