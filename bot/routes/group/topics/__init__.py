from aiogram import Router, F

from bot.routes.group.topics.close_topic import close_topic
from bot.routes.group.topics.create_topic import create_topic
from bot.routes.group.topics.edit_topic import edit_topic

router = Router()

router.message.register(create_topic, F.forum_topic_created)
router.message.register(edit_topic, F.forum_topic_edited)
router.message.register(close_topic, F.forum_topic_closed)
