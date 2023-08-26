from aiogram import Dispatcher
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from bot.models.config.config import Config
from .config import ConfigMiddleware
from .load_data import LoadDataMiddleware
from .logging import LoggingMiddleware
from .db import DBMiddleware
from .trottling import ThrottlingMiddleware


def setup_middlewares(dp: Dispatcher, pool: async_sessionmaker[AsyncSession], config_: Config):
    for tmp in [dp.message, dp.callback_query, dp.my_chat_member, dp.error]:
        tmp.middleware(LoggingMiddleware())
        tmp.middleware(ConfigMiddleware(config_))
        tmp.middleware(DBMiddleware(pool))
        tmp.middleware(LoadDataMiddleware())
        tmp.middleware(ThrottlingMiddleware())
