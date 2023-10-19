from typing import List

from aiogram import Bot
from aiogram.exceptions import AiogramError
from aiogram.types import Message
from sqlalchemy.orm import selectinload

from bot.messages.group import DELETED_MEMBERS
from bot.models import User
from bot.repositories.uow import UnitOfWork


async def clear(message: Message, uow: UnitOfWork, bot: Bot):
    users = await uow.users.get(options=[selectinload(User.groups)])
    deleted: List[User] = []
    for user in users:
        for group in user.groups:
            try:
                await bot.get_chat_member(group.id, user.id)
            except AiogramError:
                user.groups.remove(group)
        if len(user.groups) == 0:
            deleted.append(user)
            await uow.users.delete(user.id)
    if len(deleted) != 0:
        await message.reply(await DELETED_MEMBERS.render_async(users=deleted))
    else:
        await message.reply("Видалених учасників немає")
