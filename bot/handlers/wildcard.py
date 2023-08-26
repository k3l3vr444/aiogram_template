import logging

from aiogram import Router
from aiogram.types import Message, CallbackQuery

wildcard_router = Router(name=__name__)

logger = logging.getLogger(__name__)


@wildcard_router.callback_query()
@wildcard_router.message()
async def __wildcard(message_or_callback: Message | CallbackQuery):
    logger.warning(f'Wildcard: {message_or_callback}')
