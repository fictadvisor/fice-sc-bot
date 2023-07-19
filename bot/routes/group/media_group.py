from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot._types import Album
from bot.models import Message as MessageModel
from bot.repositories.message import MessageRepository


async def media_group(message: Message, session: AsyncSession, album: Album):
    message_repository = MessageRepository(session)
    for media in album.messages:
        content, media_type = Album.get_content(media)
        message_model = MessageModel(
            chat_id=media.chat.id,
            message_id=media.message_id,
            from_user_id=media.from_user.id,
            file_id=content.file_id,
            media_type=media_type,
            media_group_id=message.media_group_id,
            html_text=media.html_text or None
        )
        await message_repository.create(message_model)
