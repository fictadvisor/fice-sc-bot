from aiogram.filters import Filter
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.repositories.message import MessageRepository, MessageFilter


class IsSent(Filter):
    async def __call__(self, message: Message, session: AsyncSession):
        message_repository = MessageRepository(session)
        sent_message = await message_repository.find_one(MessageFilter(
            forward_from_chat_id=message.chat.id,
            forward_from_message_id=message.reply_to_message.message_id
        ))

        if sent_message and message.from_user.id == sent_message.from_user_id:
            return {"sent_message": sent_message}
        return None
