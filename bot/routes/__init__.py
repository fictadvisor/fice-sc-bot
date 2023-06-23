from aiogram import Router

from bot.routes.group import router as group_router

router = Router()

router.include_router(group_router)
