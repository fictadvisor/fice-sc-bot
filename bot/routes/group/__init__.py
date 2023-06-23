from aiogram import F, Router
from aiogram.enums.chat_type import ChatType
from aiogram.filters import (
    JOIN_TRANSITION,
    LEAVE_TRANSITION,
    ChatMemberUpdatedFilter, Command,
)

from .all_members import all_members
from .group_members import group_members
from .kick_member import kick_member
from .invite_bot import invite_bot
from .invite_member import invite_member
from .kick_bot import kick_bot
from .messages import messages

router = Router()

router.message.filter(F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}))

router.my_chat_member.register(invite_bot, ChatMemberUpdatedFilter(JOIN_TRANSITION))
router.chat_member.register(invite_member, ChatMemberUpdatedFilter(JOIN_TRANSITION), ~F.is_bot)

router.my_chat_member.register(kick_bot, ChatMemberUpdatedFilter(LEAVE_TRANSITION))
router.chat_member.register(kick_member, ChatMemberUpdatedFilter(LEAVE_TRANSITION), ~F.is_bot)

router.message.register(all_members, Command("all"))
router.message.register(group_members, Command("users"))

router.message.register(messages, ~F.is_bot)
