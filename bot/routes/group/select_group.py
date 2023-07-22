from aiogram import Bot
from aiogram.types import CallbackQuery

from bot.keyboards.inline.topic_keyboard import get_topic_keyboard
from bot.keyboards.inline.types.select_group import SelectGroup
from bot.messages.group import SENT, SELECT_TOPIC
from bot.repositories.topic import TopicFilter
from bot.repositories.uow import UnitOfWork
from bot.services.message import MessageService


async def select_group(callback: CallbackQuery, callback_data: SelectGroup, bot: Bot, uow: UnitOfWork) -> None:
    if not await uow.topics.check_exists(TopicFilter(group_id=callback_data.chat_id)):
        message_service = MessageService(bot, uow)
        await message_service.send_to_group(
            callback_data.chat_id,
            callback.message
        )

        await callback.message.edit_text(
            await SENT.render_async(title=message_service.get_chat_title(), status=message_service.get_status()))
        return

    topics = await uow.topics.find(TopicFilter(group_id=callback_data.chat_id))
    await callback.message.edit_text(
        SELECT_TOPIC,
        reply_markup=await get_topic_keyboard(callback_data.chat_id, topics)
    )
