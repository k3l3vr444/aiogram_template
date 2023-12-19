import asyncio
import html
import logging
import pprint
import traceback

from aiogram import Router, Bot
from aiogram.types import ErrorEvent

from bot.models.config import Config

error_router = Router(name=__name__)

logger = logging.getLogger(__name__)


def split_nice(text: str, limit: int, first_string_limit: int = 0):
    split_text = []
    tmp_limit = 0
    while len(text) > limit:
        if first_string_limit:
            tmp_limit = limit
            limit = first_string_limit
        tmp = text[:limit]
        tmp = tmp[: tmp.rfind("\n")]
        split_text.append(tmp)
        text = text[len(tmp) :]
        if first_string_limit:
            limit = tmp_limit
            first_string_limit = 0
    if len(text) > 0:
        split_text.append(text)
    return split_text


async def paginate_message(bot: Bot, chat_id: int, text: str, pre_text: str):
    # 4048 = 4096-len(html markdown)
    for index, text in enumerate(
        split_nice(text, limit=4048, first_string_limit=4048 - len(pre_text))
    ):
        if index == 0:
            await bot.send_message(
                chat_id=chat_id,
                text=f'{pre_text}<pre><code class="language-python">{text}</code></pre>',
            )
        else:
            await bot.send_message(
                chat_id=chat_id,
                text=f'<pre><code class="language-python">{text}</code></pre>',
            )
        await asyncio.sleep(0.3)


@error_router.error()
async def error_handler(event: ErrorEvent, config: Config, bot: Bot):
    logger.exception(event.exception)
    if not config.bot.error_handler_id:
        return
    for chat_id in config.bot.error_handler_id:
        if event:
            await paginate_message(
                bot=bot,
                chat_id=chat_id,
                text=pprint.pformat(event.update.model_dump(exclude_none=True)),
                pre_text="By processing update ",
            )
        await paginate_message(
            bot=bot,
            chat_id=chat_id,
            text=html.escape(traceback.format_exc()),
            pre_text="Received exception:\n\n",
        )
