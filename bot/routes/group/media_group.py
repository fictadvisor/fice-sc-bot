from aiogram.types import Message

from bot._types import Album
from bot.models import Message as MessageModel
from bot.repositories.uow import UnitOfWork


async def media_group(message: Message, uow: UnitOfWork, album: Album):
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
        await uow.messages.create(message_model)
