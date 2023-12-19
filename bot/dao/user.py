import datetime

from aiogram.types import User as AiogramUser
from sqlalchemy.dialects.postgresql import insert

from sqlalchemy.ext.asyncio import AsyncSession

from bot.dao.base import BaseDAO
from bot.models.db import User


class UserDAO(BaseDAO[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def upsert(self, aiogram_user: AiogramUser) -> User:
        kwargs = dict(
            id=aiogram_user.id,
            full_name=aiogram_user.full_name,
            username=aiogram_user.username,
            last_seen=datetime.datetime.now(),
        )
        user = await self.session.execute(
            insert(User)
            .values(**kwargs)
            .on_conflict_do_update(
                index_elements=(User.id,), set_=kwargs, where=User.id == aiogram_user.id
            )
            .returning(User)
        )
        return user.scalar_one()
