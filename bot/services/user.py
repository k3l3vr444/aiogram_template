import logging
from typing import AsyncIterator

from aiogram.types import User as AiogramUser

from bot.dao import UserDAO
from bot.models import dto

logger = logging.getLogger(__name__)


async def select_user(user_dao: UserDAO,
                      user_id: int) -> dto.User:
    user = await user_dao.get_by_id(user_id)
    return user.to_dto()


async def update_user(user_dao: UserDAO,
                      user_id: int,
                      **kwargs):
    await user_dao.update_by_id(user_id, **kwargs)
    await user_dao.commit()


async def upsert_user(user_dao: UserDAO,
                      aiogram_user: AiogramUser) -> dto.User:
    user = await user_dao.upsert_user(aiogram_user=aiogram_user)
    await user_dao.commit()
    return user.to_dto()


async def paginate_users(user_dao: UserDAO) -> AsyncIterator[dto.User]:
    async for user in user_dao.iter_all():
        yield user.to_dto()
