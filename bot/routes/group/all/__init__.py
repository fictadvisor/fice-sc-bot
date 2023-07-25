from aiogram import Router, F

from bot.routes.group.all.messages import messages

router = Router()

router.message.register(messages, ~F.is_bot)
