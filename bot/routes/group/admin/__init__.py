from aiogram import Router, F
from aiogram.filters import Command

from bot.routes.group.admin.delete_user import delete_user

router = Router()

router.message.register(delete_user, Command("delete", magic=F.args))
