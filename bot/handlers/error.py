import asyncio
import logging
import pprint
import traceback

from aiogram import Router, Bot
from aiogram.types import ErrorEvent

from bot.models.config.config import Config

error_router = Router(name=__name__)

logger = logging.getLogger(__name__)


def split_nice(text: str, limit: int):
    split_text = []
    while len(text) > limit:
        tmp = text[:limit]
        tmp = tmp[:tmp.rfind('\n')]
        split_text.append(tmp)
        text = text[len(tmp):]
    if len(text) > 0:
        split_text.append(text)
    return split_text


@error_router.error()
async def error_handler(event: ErrorEvent, config: Config, bot: Bot):
    logger.critical("Critical error caused by %s", event.exception, exc_info=True)
    for chat_id in config.bot.error_handler_id:
        update = pprint.pformat(event.update.model_dump(exclude_none=True))[:4070]
        await bot.send_message(chat_id=chat_id,
                               text=f'By processing update <pre language="python">{update}</pre>'
                               )
        for index, text in enumerate(split_nice(traceback.format_exc(), 4040)):
            await asyncio.sleep(0.3)
            if index == 0:
                await bot.send_message(chat_id=chat_id,
                                       text=f'Received exception:\n\n<pre language="python">{text}</pre>'
                                       )
            else:
                await bot.send_message(chat_id=chat_id,
                                       text=f'<pre language="python">{text}</pre>'
                                       )
