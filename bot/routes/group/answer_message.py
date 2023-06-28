from aiogram import Bot
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.messages.group import FORWARD_MESSAGE
from bot.repositories.message import MessageRepository, MessageFilter
from bot.models import Message as MessageModel


async def answer_message(message: Message, bot: Bot, session: AsyncSession) -> None:
    message_repository = MessageRepository(session)

    print(message)
    message_in = await message_repository.find_one(MessageFilter(
        chat_id=message.chat.id,
        message_id=message.reply_to_message.message_id
    ))
    print(message_in)
    if message_in is None:
        return

    user = await bot.get_chat_member(
        message.chat.id,
        message_in.from_user_id
    )

    message_out = await bot.send_message(
        chat_id=message_in.forward_from_chat_id,
        text=await FORWARD_MESSAGE.render_async(
            title=message.chat.title,
            username=user.user.mention_html(),
            text=message.html_text
        ),
        reply_to_message_id=message_in.forward_from_message_id
    )

    message_model = MessageModel(
        chat_id=message_out.chat.id,
        message_id=message_out.message_id,
        from_user_id=message.from_user.id,
        forward_from_chat_id=message.chat.id,
        forward_from_message_id=message.message_id
    )

    await message_repository.create(message_model)
