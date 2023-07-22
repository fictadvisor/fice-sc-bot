from aiogram import Router, F

from bot.keyboards.inline.types.change_status import ChangeStatus
from bot.keyboards.inline.types.select_status import SelectStatus
from bot.routes.group.status.change_status import change_status
from bot.routes.group.status.select_status import select_status

router = Router()

router.callback_query.register(change_status, ChangeStatus.filter())
router.callback_query.register(select_status, SelectStatus.filter())
