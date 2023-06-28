from aiogram import Bot
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboards.inline.types.send_message import SendMessage
from bot.messages.group import FORWARD_MESSAGE, SENT
from bot.models.message import Message
from bot.repositories.message import MessageRepository, MessageFilter


async def send_to_group(callback: CallbackQuery, callback_data: SendMessage, bot: Bot, session: AsyncSession) -> None:
    message_repository = MessageRepository(session)

    message_in = await message_repository.find_one(MessageFilter(
        chat_id=callback.message.chat.id,
        message_id=callback_data.message_id
    ))
    if message_in is None:
        return

    user = await bot.get_chat_member(
        callback.message.chat.id,
        message_in.from_user_id
    )

    messages = []
    if message_in.text:
        messages.append(await bot.send_message(
            callback_data.chat_id,
            await FORWARD_MESSAGE.render_async(
                title=callback.message.chat.title,
                username=user.user.mention_html(),
                text=message_in.text
            )
        ))
    else:
        messages.append(await bot.send_message(
            callback_data.chat_id,
            await FORWARD_MESSAGE.render_async(
                title=callback.message.chat.title,
                username=user.user.mention_html(),
            )
        ))
        messages.append(await bot.copy_message(
            callback_data.chat_id,
            callback.message.chat.id,
            callback_data.message_id
        ))

    for message_out in messages:
        message_model = Message(
            chat_id=callback_data.chat_id,
            message_id=message_out.message_id,
            from_user_id=user.user.id,
            forward_from_chat_id=callback.message.chat.id,
            forward_from_message_id=callback_data.message_id
        )

        await message_repository.create(message_model)

    title = messages[0].chat.title
    await callback.message.edit_text(await SENT.render_async(title=title))
