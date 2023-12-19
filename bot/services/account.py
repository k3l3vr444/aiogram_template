from typing import TYPE_CHECKING, AsyncIterator

from bot.dao.holder import HolderDAO

if TYPE_CHECKING:
    import aiogram
    from bot.models import dto


class AccountService:
    def __init__(self, dao: HolderDAO):
        self.dao = dao

    async def upsert_user(self, aiogram_user: "aiogram.types.User") -> "dto.User":
        user = await self.dao.user.upsert(aiogram_user=aiogram_user)
        await self.dao.commit()
        return user.to_dto()

    async def update_user(self, user_id: int, **kwargs):
        await self.dao.user.update_by_id(user_id, **kwargs)
        await self.dao.commit()

    async def paginate_users(self) -> AsyncIterator["dto.User"]:
        async for user in self.dao.user.iter_all():
            yield user.to_dto()
