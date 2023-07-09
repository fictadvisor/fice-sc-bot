from typing import Optional, Tuple

from aiogram.types import Message

from bot.types import Media, MediaTypes


def get_content(message: Message) -> Optional[Tuple[Media, MediaTypes]]:
    if message.photo:
        return message.photo[-1], MediaTypes.PHOTO
    if message.video:
        return message.video, MediaTypes.VIDEO
    if message.audio:
        return message.audio, MediaTypes.AUDIO
    if message.document:
        return message.document, MediaTypes.DOCUMENT
    return None
