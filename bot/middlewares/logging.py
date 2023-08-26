import logging
from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery, ChatMemberUpdated, ChatMemberBanned, ChatMemberMember, \
    ErrorEvent

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: dict[str, Any]
    ) -> Any:
        if type(event) == Message:
            event: Message
            try:
                logger.info(f"Received message from User[ID:{event.from_user.id}] | {event.text} ")
            except UnicodeEncodeError:
                logger.info(f"Failed to log message from User[ID:{event.from_user.id}] | UnicodeEncodeError ")
        elif type(event) == CallbackQuery:
            event: CallbackQuery
            if event.message:
                logger.info(f"Received callback query "
                            f"from User[ID:{event.from_user.id}] "
                            f"with data: {event.data}")
        elif type(event) == ChatMemberUpdated:
            event: ChatMemberUpdated
            if type(event.new_chat_member) == ChatMemberMember:
                logger.info(f"User[ID:{event.from_user.id}] joined bot")
            elif type(event.new_chat_member) == ChatMemberBanned:
                logger.info(f"User[ID:{event.from_user.id}] banned bot")
            else:
                logger.info(f"Received unknown ChatMemberUpdated :{event}")
        elif type(event) == ErrorEvent:
            pass
        else:
            logger.warning(f"Received unknown event\n{event}")
        await handler(event, data)
