from aiogram import F, Router
from aiogram.enums.chat_type import ChatType
from aiogram.filters import (
    JOIN_TRANSITION,
    LEAVE_TRANSITION,
    ChatMemberUpdatedFilter, Command,
)

from .all_members import all_members
from .answer_message import answer_message
from .group_members import group_members
from .groups_members import groups_members
from .invite_bot import invite_bot
from .invite_member import invite_member
from .kick_bot import kick_bot
from .kick_member import kick_member
from .media_group import media_group
from .messages import messages
from .rename_group import rename_group
from .send import send
from .send_to_group import send_to_group
from ...keyboards.inline.types.send_message import SendMessage

router = Router()

router.message.filter(F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}))

router.my_chat_member.register(invite_bot, ChatMemberUpdatedFilter(JOIN_TRANSITION))
router.chat_member.register(invite_member, ChatMemberUpdatedFilter(JOIN_TRANSITION), ~F.is_bot)

router.my_chat_member.register(kick_bot, ChatMemberUpdatedFilter(LEAVE_TRANSITION))
router.chat_member.register(kick_member, ChatMemberUpdatedFilter(LEAVE_TRANSITION), ~F.is_bot)

router.message.register(all_members, Command("all"))
router.message.register(groups_members, Command("groups"))
router.message.register(group_members, Command("users"))
router.message.register(send, Command("send"), F.reply_to_message)

router.callback_query.register(send_to_group, SendMessage.filter())

router.message.register(rename_group, F.new_chat_title)

router.message.register(answer_message, F.reply_to_message.from_user.is_bot)

router.message.register(media_group, F.media_group_id)

router.message.register(messages, ~F.is_bot)
