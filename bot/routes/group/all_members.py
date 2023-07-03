from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.messages.group import ALL_MEMBERS
from bot.repositories.user import UserRepository


async def all_members(message: Message, session: AsyncSession):
    user_repository = UserRepository(session)
    users = await user_repository.get()

    await message.answer(await ALL_MEMBERS.render_async(users=users))
