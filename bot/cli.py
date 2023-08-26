import asyncio
import datetime
import logging
import os
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage

from bot.config import load_config
from bot.filters.chat_type import PrivateChatTypeFilter
from bot.filters.superuser import AdminFilter
from bot.handlers.admin import admin_router
from bot.handlers.admin.commands import admin_command_router
from bot.handlers.error import error_router
from bot.handlers.user import user_router
from bot.handlers.user.commands import user_command_router
from bot.handlers.wildcard import wildcard_router
from bot.middlewares import setup_middlewares
from bot.models.db.db import create_pool
from bot.scheduler import scheduler_template

logger = logging.getLogger(__name__)


async def main():
    config = load_config(Path(__file__).parent.parent)
    logging_handlers = [logging.StreamHandler()]
    if config.logger.use_file_handler:
        try:
            os.mkdir("logs")
        except FileExistsError:
            pass
        logging_handlers.append(logging.FileHandler(f"logs/{datetime.datetime.now().strftime('%Y_%m_%d-%H_%M')}.log"))
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s.%(msecs)03d | %(name)-30s | %(levelname)-8s | #%(lineno)-5d| %(message)s \n",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=logging_handlers
    )
    logger.warning("Starting bot")

    if config.bot.use_redis:
        storage = RedisStorage.from_url('redis://@localhost:6379')
        logger.info("Using redis storage")
    else:
        storage = MemoryStorage()
        logger.info("Using memory storage")

    dp = Dispatcher(storage=storage)

    engine, pool = create_pool(config.db)

    setup_middlewares(dp, pool, config)

    logging.warning(f"Admin list: {config.bot.admin_id}")

    admin_filter = AdminFilter(config.bot.admin_id)
    admin_router.message.filter(admin_filter)
    admin_command_router.message.filter(admin_filter)

    for router in [admin_command_router, user_command_router, admin_router, user_router, wildcard_router, error_router]:
        router.message.filter(PrivateChatTypeFilter())
        dp.include_router(router)
    logger.debug("handlers configured successfully")

    bot = Bot(
        token=config.bot.token,
        parse_mode="HTML",
    )

    loop = asyncio.get_event_loop()
    loop.create_task(scheduler_template(bot=bot, session_pool=pool))

    # start
    logger.info("started")
    try:
        await dp.start_polling(bot)
    finally:
        await engine.dispose()
        logger.info("stopped")


def cli():
    """Wrapper for command line"""
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
