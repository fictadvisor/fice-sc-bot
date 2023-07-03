from aiogram import Bot
from aiogram.types import BotCommandScopeAllGroupChats, BotCommand


async def set_commands(bot: Bot) -> None:
    uk_commands = [
        (
            (
                BotCommand(command="all", description="Усі учасники"),
                BotCommand(command="groups", description="Учасники груп"),
                BotCommand(command="users", description="Учасники чату"),
                BotCommand(command="send", description="Надіслати повідомлення"),
            ),
            BotCommandScopeAllGroupChats(),
        )
    ]

    for commands, scope in uk_commands:
        await bot.set_my_commands(commands=commands, scope=scope)