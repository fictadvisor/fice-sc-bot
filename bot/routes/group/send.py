from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards.inline.send_keyboard import get_send_keyboard
from bot.messages.group import SELECT_GROUP
from bot.repositories.group import GroupRepository
from bot.repositories.message import MessageRepository
from bot.models import Message as MessageModel


async def send(message: Message, session: AsyncSession) -> None:
    group_repository = GroupRepository(session)
    groups = await group_repository.get()

    message_repository = MessageRepository(session)
    message_model = MessageModel(
        chat_id=message.chat.id,
        message_id=message.reply_to_message.message_id,
        from_user_id=message.reply_to_message.from_user.id,
        text=message.reply_to_message.html_text
    )
    await message_repository.create(message_model)

    await message.answer(
        text=SELECT_GROUP,
        reply_markup=await get_send_keyboard(groups, message.reply_to_message.message_id)
    )
