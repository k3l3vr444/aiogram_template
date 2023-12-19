import logging

from aiogram import Router
from aiogram.types import Message, CallbackQuery

wildcard_router = Router(name=__name__)

logger = logging.getLogger(__name__)


@wildcard_router.callback_query()
@wildcard_router.message()
async def __wildcard(event: Message | CallbackQuery):
    logger.warning(f"Wildcard: {event}")
