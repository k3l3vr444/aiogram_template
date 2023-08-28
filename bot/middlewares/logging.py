import logging
from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject, Message, CallbackQuery, ChatMemberUpdated, ChatMemberBanned, ChatMemberMember, \
    ErrorEvent, Update

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: dict[str, Any]
    ) -> Any:
        update: Update = data['event_update']
        update_id = update.update_id
        state: FSMContext = data['state']
        current_state = await state.get_state()
        if type(event) == Message:
            event: Message
            try:
                logger.info(f"Received message from User[ID:{event.from_user.id}] | Update[ID: {update_id}] | "
                            f"State: {current_state} | Text: '{event.text}'")
            except UnicodeEncodeError:
                logger.info(f"Failed to log message from User[ID:{event.from_user.id}] | Update[ID: {update_id}] |"
                            f"State: {current_state} | UnicodeEncodeError ")
        elif type(event) == CallbackQuery:
            event: CallbackQuery
            if event.message:
                logger.info(f"Received callback query "
                            f"from User[ID:{event.from_user.id}]  | Update[ID: {update_id}] | State: {current_state} | "
                            f"Data: {event.data}")
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
        return await handler(event, data)
