from aiogram import Router
from aiogram.filters import Command

from bot.routes.group.random_coffee.generate_coffee import generate_coffee

router = Router()

router.message.register(generate_coffee, Command("generate_coffee"))
