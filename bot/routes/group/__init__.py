from aiogram import F, Router
from aiogram.enums.chat_type import ChatType
from aiogram.filters import (
    JOIN_TRANSITION,
    LEAVE_TRANSITION,
    ChatMemberUpdatedFilter, Command, MagicData, ExceptionMessageFilter,
)

from .all_members import all_members
from .answer_message import answer_message
from .clear import clear
from .errors import errors
from .group_members import group_members
from .groups_members import groups_members
from .help_command import help_command
from .invite_bot import invite_bot
from .invite_member import invite_member
from .kick_bot import kick_bot
from .kick_member import kick_member
from .media_group import media_group
from .rename_group import rename_group
from .reply_message import reply_message
from .responsible import responsible
from .select_group import select_group
from .select_topic import select_topic
from .select_type import select_type
from .send import send
from .topic_not_found import topic_not_found
from .topics import router as topics_router
from .status import router as status_router
from .admin import router as admin_router
from .all import router as all_router
from .random_coffee import router as random_coffee_router
from ...filters.is_sent import IsSent
from ...keyboards.inline.types.select_group import SelectGroup
from ...keyboards.inline.types.select_topic import SelectTopic
from ...keyboards.inline.types.select_type import SelectType

router = Router()

router.include_router(random_coffee_router)
router.include_router(admin_router)
router.include_router(topics_router)
router.include_router(status_router)
router.include_router(all_router)

router.message.filter(F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}))

router.my_chat_member.register(invite_bot, ChatMemberUpdatedFilter(JOIN_TRANSITION))
router.chat_member.register(invite_member, ChatMemberUpdatedFilter(JOIN_TRANSITION), ~F.new_chat_member.is_bot)

router.my_chat_member.register(kick_bot, ChatMemberUpdatedFilter(LEAVE_TRANSITION))
router.chat_member.register(kick_member, ChatMemberUpdatedFilter(LEAVE_TRANSITION), ~F.new_chat_member.is_bot)

router.message.register(all_members, Command("all"))
router.message.register(groups_members, Command("groups"))
router.message.register(group_members, Command("users"))
router.message.register(send, Command("send"), F.reply_to_message)
router.message.register(responsible, Command("responsible", magic=F.args), F.chat.is_forum)
router.message.register(help_command, Command("help"))
router.message.register(clear, Command("clear"))

router.callback_query.register(select_type, SelectType.filter())
router.callback_query.register(select_group, SelectGroup.filter())
router.callback_query.register(select_topic, SelectTopic.filter())

router.message.register(rename_group, F.new_chat_title)

router.message.register(answer_message, MagicData(F.event.reply_to_message.from_user.id == F.bot.id))

router.message.register(reply_message, MagicData(F.event.reply_to_message.from_user.id != F.bot.id), IsSent())

router.message.register(media_group, F.media_group_id)

router.errors.register(topic_not_found,
                       ExceptionMessageFilter("Telegram server says Bad Request: message thread not found"))

router.errors.register(errors)
