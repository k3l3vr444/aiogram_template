import asyncio
import logging

from aiogram import Bot
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

logger = logging.getLogger(__name__)


async def scheduler_template(bot: Bot, session_pool: async_sessionmaker[AsyncSession]):
    while True:
        async with session_pool() as session:
            pass
            await asyncio.sleep(60)
