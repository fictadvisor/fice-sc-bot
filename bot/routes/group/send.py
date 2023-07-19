from aiogram.types import Message

from bot.keyboards.inline.send_keyboard import get_send_keyboard
from bot.messages.group import SELECT_GROUP
from bot.models import Message as MessageModel
from bot.repositories.uow import UnitOfWork


async def send(message: Message, uow: UnitOfWork) -> None:
    groups = await uow.groups.get()

    if not message.reply_to_message.media_group_id:
        message_model = MessageModel(
            chat_id=message.chat.id,
            message_id=message.reply_to_message.message_id,
            from_user_id=message.reply_to_message.from_user.id,
            html_text=message.reply_to_message.html_text
        )
        await uow.messages.create(message_model)

    await message.reply(
        text=SELECT_GROUP,
        reply_markup=await get_send_keyboard(
            list(filter(lambda group: group.id != message.chat.id, groups)),
            message.reply_to_message.message_id
        )
    )
