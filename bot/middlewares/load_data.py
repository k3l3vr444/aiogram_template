from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from bot.services.holder import ServiceHolder


class LoadDataMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        service: ServiceHolder = data["service"]
        data["user"] = await service.account.upsert_user(
            aiogram_user=data["event_from_user"]
        )
        return await handler(event, data)
