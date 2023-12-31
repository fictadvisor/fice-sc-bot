from aiogram.filters import Filter
from aiogram.types import Message

from bot.repositories.message import MessageFilter
from bot.repositories.uow import UnitOfWork


class IsSent(Filter):
    async def __call__(self, message: Message, uow: UnitOfWork):
        sent_message = await uow.messages.find_one(MessageFilter(
            forward_from_chat_id=message.chat.id,
            forward_from_message_id=message.reply_to_message.message_id
        ))

        if sent_message and message.from_user.id == sent_message.from_user_id:
            return {"main_message": sent_message}
        return None
