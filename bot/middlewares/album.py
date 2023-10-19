from asyncio import sleep
from typing import (
    Any, Callable, Awaitable, MutableMapping,
    Dict, List
)

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from cachetools import TTLCache

from bot._types import Album


class AlbumMiddleware(BaseMiddleware):
    DEFAULT_LATENCY = 0.3
    DEFAULT_TTL = 1

    def __init__(
            self,
            latency: float = DEFAULT_LATENCY,
            ttl: float = DEFAULT_TTL
    ) -> None:
        self.latency = latency
        self.cache: MutableMapping[str, List[Any]] = TTLCache(maxsize=10_000, ttl=ttl)

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        if isinstance(event, Message) and event.media_group_id is not None:
            key = event.media_group_id

            if key in self.cache:
                self.cache[key].append(event)
                return

            self.cache[key] = [event]

            await sleep(self.latency)
            data["album"] = Album.create_from_messages(self.cache[key])

        return await handler(event, data)
