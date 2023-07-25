from aiogram.types import Message

from bot.messages.group import HELP


async def help_command(message: Message):
    await message.answer(HELP)
