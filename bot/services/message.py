from asyncio import sleep
from typing import List, Optional

from aiogram import Bot
from aiogram.types import Message, InputMedia, User

from bot._types import INPUT_TYPES, Album
from bot.messages.group import FORWARD_MESSAGE
from bot.models import Message as MessageModel
from bot.repositories.message import MessageFilter
from bot.repositories.uow import UnitOfWork


class MessageService:
    messages: List[Message]
    bot: Bot
    uow: UnitOfWork

    def __init__(self, bot: Bot, uow: UnitOfWork):
        self.bot = bot
        self.uow = uow
        self.messages = []

    async def send_to_group(self, chat_id: int, title: str, message_id: int, from_chat_id: int):
        message_in = await self.uow.messages.find_one(MessageFilter(
            chat_id=from_chat_id,
            message_id=message_id,
        ), order=[MessageModel.id.desc()])
        if message_in is None:
            return

        user = await self._get_user_by_chat_and_user_id(chat_id, message_in.from_user_id)
        username = self._get_username_from_user(user)

        if message_in.media_group_id:
            messages = await self.uow.messages.find(MessageFilter(
                chat_id=chat_id,
                media_group_id=message_in.media_group_id
            ))

            await self._send_media_group(chat_id, title, username, self._get_media_group_from_message_models(messages))
        elif message_in.html_text:
            await self._send_text(chat_id, title, username, message_in.html_text)
        else:
            await self._copy_message(chat_id, title, username, from_chat_id, message_in.message_id)

        await self._save_messages(chat_id, message_id, user.id, from_chat_id)

    async def reply_message(self, message: Message, main_message: MessageModel, album: Optional[Album] = None):
        username = self._get_username_from_user(message.from_user)
        if message.media_group_id:
            await self._send_media_group(main_message.chat_id, message.chat.title,
                                         username, album.as_media_group, main_message.message_id)
        elif message.text:
            await self._send_text(main_message.chat_id, message.chat.title, username, message.html_text,
                                  main_message.message_id)
        else:
            await self._copy_message(main_message.chat_id, message.chat.title, username, message.chat.id,
                                     message.message_id, main_message.message_id)
        await self._save_messages(main_message.chat_id, message.message_id, message.from_user.id, message.chat.id)

    async def answer_message(self, message: Message, album: Optional[Album] = None):
        message_in = await self.uow.messages.find_one(MessageFilter(
            chat_id=message.chat.id,
            message_id=message.reply_to_message.message_id
        ))
        if message_in is None:
            return

        username = self._get_username_from_user(message.from_user)
        if message.media_group_id:
            await self._send_media_group(message_in.forward_from_chat_id, message.chat.title, username,
                                         album.as_media_group, message_in.forward_from_message_id)
        elif message.html_text:
            await self._send_text(message_in.forward_from_chat_id, message.chat.title, username, message.html_text,
                                  message_in.forward_from_message_id)
        else:
            await self._copy_message(message_in.forward_from_chat_id, message.chat.title, username, message.chat.id,
                                     message.message_id, message_in.forward_from_message_id)
        await self._save_messages(message_in.forward_from_chat_id, message.message_id, message.from_user.id,
                                  message.chat.id)

    async def _send_media_group(self, chat_id: int, chat_title: str, username: str, media_group: List[InputMedia],
                                reply_to_message_id: Optional[int] = None) -> None:
        await self._send_text(chat_id, chat_title, username, None, reply_to_message_id)
        await sleep(0.1)
        self.messages.extend(await self.bot.send_media_group(
            chat_id=chat_id,
            media=media_group,
            reply_to_message_id=reply_to_message_id
        ))

    async def _send_text(self, chat_id: int, chat_title: str, username: str, html_text: Optional[str] = None,
                         reply_to_message_id: Optional[int] = None) -> None:
        self.messages.append(await self.bot.send_message(
            chat_id=chat_id,
            text=await FORWARD_MESSAGE.render_async(
                title=chat_title,
                username=username,
                html_text=html_text
            ),
            reply_to_message_id=reply_to_message_id
        ))

    async def _copy_message(self, chat_id: int, chat_title: str, username: str, from_chat_id: int, message_id: int,
                            reply_to_message_id: Optional[int] = None) -> None:
        self.messages.append(await self.bot.send_message(
            chat_id,
            await FORWARD_MESSAGE.render_async(
                title=chat_title,
                username=username,
            ),
            reply_to_message_id=reply_to_message_id
        ))
        await sleep(0.1)
        self.messages.append(await self.bot.copy_message(
            chat_id=chat_id,
            from_chat_id=from_chat_id,
            message_id=message_id,
            reply_to_message_id=reply_to_message_id
        ))

    async def _get_user_by_chat_and_user_id(self, chat_id: int, user_id: int):
        return (await self.bot.get_chat_member(chat_id, user_id)).user

    @staticmethod
    def _get_username_from_user(user: User) -> str:
        return f"@{user.username}" if user.username else user.full_name

    @staticmethod
    def _get_media_group_from_message_models(messages: List[MessageModel]) -> List[InputMedia]:
        return [INPUT_TYPES[media.media_type](
            type=media.media_type,
            media=media.file_id,
            caption=media.html_text
        ) for media in messages]

    async def _save_messages(self, chat_id: int, from_message_id: int, user_id: int, from_chat_id: int):
        for message_out in self.messages:
            message_model = MessageModel(
                chat_id=chat_id,
                message_id=message_out.message_id,
                from_user_id=user_id,
                forward_from_chat_id=from_chat_id,
                forward_from_message_id=from_message_id
            )

            await self.uow.messages.create(message_model)

    def get_chat_title(self) -> str:
        return self.messages[0].chat.title
