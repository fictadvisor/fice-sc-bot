import logging
import traceback
from asyncio import sleep

from aiogram import Bot
from aiogram.types import ErrorEvent

from bot.settings import settings


async def errors(event: ErrorEvent, bot: Bot):
    if event.update.message:
        await bot.copy_message(settings.ADMIN_ID, event.update.message.chat.id, event.update.message.message_id)
        tb = ''.join(traceback.format_exception(None, event.exception, event.exception.__traceback__))
        for sub in [tb[i:i + 4096] for i in range(0, len(tb), 4096)]:
            await bot.send_message(settings.ADMIN_ID, sub, parse_mode=None)
            await sleep(0.1)
    logging.error(event.exception)
