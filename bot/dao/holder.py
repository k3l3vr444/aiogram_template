from dataclasses import dataclass, field

from sqlalchemy.ext.asyncio import AsyncSession

from bot.dao import UserDAO


@dataclass
class HolderDAO:
    session: AsyncSession
    user: UserDAO = field(init=False)

    def __post_init__(self):
        self.user = UserDAO(self.session)

    async def commit(self):
        await self.session.commit()
