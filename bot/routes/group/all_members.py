from aiogram.types import Message

from bot.messages.group import ALL_MEMBERS
from bot.repositories.uow import UnitOfWork


async def all_members(message: Message, uow: UnitOfWork):
    users = await uow.users.get()

    await message.answer(await ALL_MEMBERS.render_async(users=users))
