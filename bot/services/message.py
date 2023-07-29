from asyncio import sleep
from typing import List, Optional

from aiogram import Bot
from aiogram.types import Message, InputMedia, User, InlineKeyboardMarkup, Chat
from sqlalchemy.orm import selectinload

from bot._types import INPUT_TYPES, Album
from bot._types.message_types import MessageTypes
from bot._types.status import Status
from bot.keyboards.inline.change_status_keyboard import get_change_status_keyboard
from bot.keyboards.inline.types.select_status import SelectStatus
from bot.messages.group import FORWARD_MESSAGE, SENT
from bot.models import Message as MessageModel, User as UserModel, Topic
from bot.repositories.message import MessageFilter
from bot.repositories.topic import TopicFilter
from bot.repositories.uow import UnitOfWork


class MessageService:
    messages: List[Message]
    bot: Bot
    uow: UnitOfWork
    status: Optional[Status]

    def __init__(self, bot: Bot, uow: UnitOfWork):
        self.bot = bot
        self.uow = uow
        self.messages = []
        self.status = None

    async def change_status(self, message: Message, callback_data: SelectStatus):
        message_out = await self.uow.messages.find_one(MessageFilter(
            chat_id=message.chat.id, message_id=message.message_id
        ))
        message_model = await self.uow.messages.find_one(
            MessageFilter(message_id=message_out.forward_from_message_id, chat_id=message_out.forward_from_chat_id))
        topic = await self.uow.topics.find_one(TopicFilter(
            group_id=message.chat.id,
            thread_id=message.message_thread_id
        ), options=[selectinload(Topic.responsible)])

        message_model.status = callback_data.status
        user = await self.get_user_by_chat_and_user_id(message_model.chat_id, message_model.from_user_id)
        chat = await self.get_chat_by_chat_id(message_model.chat_id)

        await message.edit_text(await FORWARD_MESSAGE.render_async(
            title=chat.title,
            username=self._get_username_from_user(user),
            html_text=message_model.html_text,
            status=callback_data.status,
            responsible=topic.responsible if topic else None
        ), reply_markup=await get_change_status_keyboard(callback_data.chat_id, callback_data.message_id))

        await self.bot.edit_message_text(
            await SENT.render_async(title=message.chat.title, status=callback_data.status), callback_data.chat_id,
            callback_data.message_id)

    async def send_to_group(self, chat_id: int, message: Message,
                            thread_id: Optional[int] = None):
        from_message = message.reply_to_message
        message_in = await self.uow.messages.find_one(MessageFilter(
            chat_id=from_message.chat.id,
            message_id=from_message.message_id,
        ), order=[MessageModel.id.desc()])
        topic = await self.uow.topics.find_one(TopicFilter(
            group_id=chat_id,
            thread_id=thread_id
        ), options=[selectinload(Topic.responsible)])

        if message_in is None:
            return

        user = await self.get_user_by_chat_and_user_id(chat_id, message_in.from_user_id)
        username = self._get_username_from_user(user)
        title = from_message.chat.title
        from_chat_id = from_message.chat.id
        responsible = topic.responsible if topic else None

        pin_message = True if message_in.type == MessageTypes.TASK else False
        reply_markup = await get_change_status_keyboard(from_chat_id, message.message_id) if message_in.type == MessageTypes.TASK else None
        self.status = message_in.status

        if message_in.media_group_id:
            messages = await self.uow.messages.find(MessageFilter(
                chat_id=chat_id,
                media_group_id=message_in.media_group_id
            ))

            media_group = self._get_media_group_from_message_models(messages)
            await self._send_media_group(chat_id, title, username, media_group, None, thread_id, reply_markup,
                                         message_in.status, responsible)
        elif message_in.html_text and not message.caption:
            await self._send_text(chat_id, title, username, message_in.html_text, None, thread_id, reply_markup,
                                  message_in.status, responsible)
        else:
            await self._copy_message(chat_id, title, username, from_chat_id, message_in.message_id, None, thread_id,
                                     reply_markup, message_in.status, responsible)

        if pin_message:
            await self.messages[0].pin()

        await self._save_messages(chat_id, from_message.message_id, user.id, from_chat_id)

    async def reply_message(self, message: Message, main_message: MessageModel, album: Optional[Album] = None):
        username = self._get_username_from_user(message.from_user)
        if message.media_group_id:
            await self._send_media_group(main_message.chat_id, message.chat.title,
                                         username, album.as_media_group, main_message.message_id)
        elif message.html_text and not message.caption:
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
        elif message.html_text and not message.caption:
            await self._send_text(message_in.forward_from_chat_id, message.chat.title, username, message.html_text,
                                  message_in.forward_from_message_id)
        else:
            await self._copy_message(message_in.forward_from_chat_id, message.chat.title, username, message.chat.id,
                                     message.message_id, message_in.forward_from_message_id)
        await self._save_messages(message_in.forward_from_chat_id, message.message_id, message.from_user.id,
                                  message.chat.id)

    async def _send_media_group(self, chat_id: int, chat_title: str, username: str, media_group: List[InputMedia],
                                reply_to_message_id: Optional[int] = None, thread_id: Optional[int] = None,
                                reply_markup: Optional[InlineKeyboardMarkup] = None,
                                status: Optional[Status] = None, responsible: Optional[UserModel] = None) -> None:
        await self._send_text(chat_id, chat_title, username, None, reply_to_message_id, thread_id, reply_markup, status, responsible)
        await sleep(0.1)
        self.messages.extend(await self.bot.send_media_group(
            chat_id,
            media_group,
            thread_id,
            reply_to_message_id=reply_to_message_id
        ))

    async def _send_text(self, chat_id: int, chat_title: str, username: str, html_text: Optional[str] = None,
                         reply_to_message_id: Optional[int] = None, thread_id: Optional[int] = None,
                         reply_markup: Optional[InlineKeyboardMarkup] = None, status: Optional[Status] = None, responsible: Optional[UserModel] = None) -> None:
        self.messages.append(await self.bot.send_message(
            chat_id,
            await FORWARD_MESSAGE.render_async(
                title=chat_title,
                username=username,
                html_text=html_text,
                status=status,
                responsible=responsible
            ),
            thread_id,
            reply_markup=reply_markup,
            reply_to_message_id=reply_to_message_id
        ))

    async def _copy_message(self, chat_id: int, chat_title: str, username: str, from_chat_id: int, message_id: int,
                            reply_to_message_id: Optional[int] = None, thread_id: Optional[int] = None,
                            reply_markup: Optional[InlineKeyboardMarkup] = None,
                            status: Optional[Status] = None, responsible: Optional[UserModel] = None) -> None:
        await self._send_text(chat_id, chat_title, username, None, reply_to_message_id, thread_id, reply_markup, status, responsible)
        await sleep(0.1)
        self.messages.append(await self.bot.copy_message(
            chat_id,
            from_chat_id,
            message_id,
            thread_id,
            reply_to_message_id=reply_to_message_id
        ))

    async def get_user_by_chat_and_user_id(self, chat_id: int, user_id: int) -> User:
        return (await self.bot.get_chat_member(chat_id, user_id)).user

    async def get_chat_by_chat_id(self, chat_id: int) -> Chat:
        return await self.bot.get_chat(chat_id)

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

    def get_status(self) -> Optional[Status]:
        return self.status
