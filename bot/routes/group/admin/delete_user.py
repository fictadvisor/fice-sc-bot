from aiogram.filters import CommandObject
from aiogram.types import Message

from bot.repositories.uow import UnitOfWork
from bot.repositories.user import UserFilter


async def delete_user(_: Message, command: CommandObject, uow: UnitOfWork):
    user = await uow.users.find_one(UserFilter(username=command.args))
    if user:
        await uow.users.delete(user.id)
