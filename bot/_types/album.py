from collections import defaultdict
from enum import Enum
from typing import List, Optional, Dict, Type, Union, cast, Tuple

from aiogram.types import (
    PhotoSize, Video, Audio,
    Document, InputMediaPhoto,
    InputMediaVideo, InputMediaAudio,
    InputMediaDocument, Message
)
from pydantic import BaseModel


class MediaTypes(str, Enum):
    PHOTO = "photo"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"


Media = Union[PhotoSize, Video, Audio, Document]
InputMedia = Union[
    InputMediaPhoto,
    InputMediaVideo,
    InputMediaAudio,
    InputMediaDocument
]
INPUT_TYPES: Dict[str, Type[InputMedia]] = {
    MediaTypes.PHOTO: InputMediaPhoto,
    MediaTypes.VIDEO: InputMediaVideo,
    MediaTypes.AUDIO: InputMediaAudio,
    MediaTypes.DOCUMENT: InputMediaDocument
}


class Album(BaseModel):
    photo: Optional[List[PhotoSize]] = None
    video: Optional[List[Video]] = None
    audio: Optional[List[Audio]] = None
    document: Optional[List[Document]] = None
    caption: Optional[str] = None
    messages: List[Message]

    @property
    def media_types(self) -> List[str]:
        return [
            media_type for media_type in INPUT_TYPES
            if getattr(self, media_type)
        ]

    @property
    def as_media_group(self) -> List[InputMedia]:
        group = [
            INPUT_TYPES[media_type](type=media_type, media=media.file_id)
            for media_type in self.media_types
            for media in getattr(self, media_type)
        ]
        if group:
            group[0].caption = self.caption

        return group

    @classmethod
    def create_from_messages(cls, messages: List[Message]) -> "Album":
        data = defaultdict(list)
        data["messages"] = messages
        for message in messages:
            media, content_type = cast(Tuple[Media, str], cls.get_content(message))
            data[content_type].append(media)
            if message.html_text is not None:
                data["caption"] = message.html_text
        return Album(**data)

    @staticmethod
    def get_content(message: Message) -> Optional[Tuple["Media", "MediaTypes"]]:
        if message.photo:
            return message.photo[-1], MediaTypes.PHOTO
        if message.video:
            return message.video, MediaTypes.VIDEO
        if message.audio:
            return message.audio, MediaTypes.AUDIO
        if message.document:
            return message.document, MediaTypes.DOCUMENT
        return None
