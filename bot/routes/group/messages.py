from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models import User
from bot.repositories.user import UserRepository


async def messages(message: Message, session: AsyncSession):
    user_repository = UserRepository(session)
    user = await user_repository.get_by_id(message.from_user.id)

    if user is None:
        user = User(
            id=message.from_user.id,
            username=f"@{message.from_user.username}" or message.from_user.mention_html()
        )
        await user_repository.create(user)
    elif user.username != message.from_user.username:
        user.username = f"@{message.from_user.username}" or message.from_user.mention_html()
