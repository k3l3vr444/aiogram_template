import logging
from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    TelegramObject,
    Message,
    CallbackQuery,
    ChatMemberUpdated,
    ChatMemberBanned,
    ChatMemberMember,
    Update,
)

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        update: Update = data["event_update"]
        update_id = update.update_id
        state: FSMContext = data["state"]
        current_state = await state.get_state()
        if isinstance(event, Message):
            event: Message
            try:
                if event.text:
                    logger.info(
                        f"Update id={update_id} | User id={event.from_user.id} | State={current_state} | "
                        f"Received message: '{event.text}'"
                    )
                elif event.photo:
                    photo = max(event.photo, key=lambda x: x.file_size).file_id
                    logger.info(
                        f"Update id={update_id} | User id={event.from_user.id} | State={current_state} | "
                        f"Received caption: '{event.caption}' | Photo: {photo}"
                    )
                elif event.video:
                    logger.info(
                        f"Update id={update_id} | User id={event.from_user.id} | State={current_state} | "
                        f"Received caption: '{event.caption}' | Video: {event.video.file_id}"
                    )
                else:
                    logger.info(
                        f"Update id={update_id} | User id={event.from_user.id} | State={current_state} | "
                        f"Received unknown message type: '{event}'"
                    )
            except UnicodeEncodeError:
                logger.info(
                    f"Update id={update_id} | User id={event.from_user.id} | State={current_state} | "
                    f"Failed to log message from  | UnicodeEncodeError "
                )
        elif isinstance(event, CallbackQuery):
            event: CallbackQuery
            if event.message:
                logger.info(
                    f"Update id={update_id} | User id={event.from_user.id} | State={current_state} | "
                    f"Received callback query: {event.data}"
                )
            else:
                logger.info(f"Received unknown CallbackQuery :{event}")
        elif isinstance(event, ChatMemberUpdated):
            event: ChatMemberUpdated
            if event.chat.type == "private":
                if isinstance(event.new_chat_member, ChatMemberMember):
                    logger.info(
                        f"Update id={update_id} | User id={event.from_user.id} | Joined bot"
                    )
                elif isinstance(event.new_chat_member, ChatMemberBanned):
                    logger.info(
                        f"Update id={update_id} | User id={event.from_user.id} | Banned bot"
                    )
                else:
                    logger.info(f"Received unknown ChatMemberUpdated :{event}")
            else:
                logger.info(f"Received unknown ChatMemberUpdated :{event}")
        else:
            logger.warning(f"Received unknown event\n{event}")
        return await handler(event, data)
