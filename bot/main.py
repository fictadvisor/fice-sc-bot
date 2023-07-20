import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from bot.commands import set_commands
from bot.middlewares.album import AlbumMiddleware
from bot.middlewares.sessionmaker import SessionMaker
from bot.routes import router
from bot.settings import settings

logging.basicConfig(level=logging.INFO)
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


async def main() -> None:
    engine = create_async_engine(
        URL.create(
            "postgresql+asyncpg",
            username=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD.get_secret_value(),
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
            database=settings.POSTGRES_DB,
        ),
        pool_recycle=1800
    )
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False, autoflush=False)

    bot = Bot(token=settings.TOKEN.get_secret_value(), parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    await set_commands(bot)

    dp.update.middleware(SessionMaker(sessionmaker))
    dp.errors.middleware(SessionMaker(sessionmaker))
    dp.message.middleware(AlbumMiddleware())

    dp.callback_query.middleware(CallbackAnswerMiddleware())

    dp.include_router(router)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
