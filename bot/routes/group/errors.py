import traceback
from asyncio import sleep

from aiogram.types import ErrorEvent


async def errors(event: ErrorEvent):
    if event.update.message:
        tb = ''.join(traceback.format_exception(None, event.exception, event.exception.__traceback__))
        for sub in [tb[i:i + 4096] for i in range(0, len(tb), 4096)]:
            await event.update.message.reply(sub, parse_mode=None)
            await sleep(0.1)
