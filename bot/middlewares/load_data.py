from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from bot.services.user import upsert_user


class LoadDataMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: dict[str, Any]
    ) -> Any:
        holder_dao = data["dao"]
        data["user"] = await upsert_user(user_dao=holder_dao.user,
                                         aiogram_user=data["event_from_user"])
        return await handler(event, data)
