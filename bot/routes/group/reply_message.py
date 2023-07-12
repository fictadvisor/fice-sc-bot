from asyncio import sleep
from typing import Optional

from aiogram import Bot
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot._types import Album
from bot.messages.group import FORWARD_MESSAGE
from bot.models import Message as MessageModel
from bot.repositories.message import MessageRepository


async def reply_message(message: Message, bot: Bot, session: AsyncSession, sent_message: MessageModel, album: Optional[Album] = None):
    message_repository = MessageRepository(session)

    messages = []
    if message.media_group_id:
        messages.append(await bot.send_message(
            sent_message.chat_id,
            await FORWARD_MESSAGE.render_async(
                title=message.chat.title,
                username=f"@{message.from_user.username}"
                if message.from_user.username
                else message.from_user.full_name,
            ),
            reply_to_message_id=sent_message.message_id
        ))
        await sleep(0.1)
        messages.extend(await bot.send_media_group(
            chat_id=sent_message.chat_id,
            media=album.as_media_group,
            reply_to_message_id=sent_message.message_id
        ))
    elif message.text:
        messages.append(await bot.send_message(
            chat_id=sent_message.chat_id,
            text=await FORWARD_MESSAGE.render_async(
                title=message.chat.title,
                username=f"@{message.from_user.username}"
                if message.from_user.username
                else message.from_user.full_name,
                text=message.html_text
            ),
            reply_to_message_id=sent_message.message_id
        ))
    else:
        messages.append(await bot.send_message(
            sent_message.chat_id,
            await FORWARD_MESSAGE.render_async(
                title=message.chat.title,
                username=f"@{message.from_user.username}"
                if message.from_user.username
                else message.from_user.full_name,
            ),
            reply_to_message_id=sent_message.message_id
        ))
        await sleep(0.1)
        messages.append(await bot.copy_message(
            chat_id=sent_message.chat_id,
            from_chat_id=message.chat.id,
            message_id=message.message_id,
            reply_to_message_id=sent_message.message_id
        ))

    for message_out in messages:
        message_model = MessageModel(
            chat_id=sent_message.chat_id,
            message_id=message_out.message_id,
            from_user_id=message.from_user.id,
            forward_from_chat_id=message.chat.id,
            forward_from_message_id=message.message_id
        )

        await message_repository.create(message_model)
