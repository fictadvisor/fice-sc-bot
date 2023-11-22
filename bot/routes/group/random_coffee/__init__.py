from aiogram import Router
from aiogram.filters import Command

from bot.routes.group.random_coffee.generate_coffee import generate_coffee
from bot.routes.group.random_coffee.my_coffee import my_coffee

router = Router()

router.message.register(generate_coffee, Command("generate_coffee"))
router.message.register(my_coffee, Command("my_coffee"))
