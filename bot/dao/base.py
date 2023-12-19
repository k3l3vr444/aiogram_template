from typing import TypeVar, Type, Generic, AsyncIterator

from sqlalchemy import delete, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from bot.models.db import Base

Model = TypeVar("Model", Base, Base)


class BaseDAO(Generic[Model]):
    def __init__(self, model: Type[Model], session: AsyncSession):
        self.model = model
        self.session = session

    async def iter_all(self) -> AsyncIterator[Model]:
        OFFSET = 0
        LIMIT = 1000
        while True:
            query = select(self.model).offset(OFFSET).limit(LIMIT)
            results = await self.session.execute(query)
            results = results.scalars().all()
            if not results:
                return
            for result in results:
                yield result
            OFFSET += len(results)

    async def get_by_id(self, id: int) -> Model:
        result = await self.session.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one()

    async def update_by_id(self, id: int, **kwargs):
        query = update(self.model).where(self.model.id == id).values(**kwargs)
        await self.session.execute(query)

    def save(self, obj: Model):
        self.session.add(obj)

    async def delete_all(self):
        await self.session.execute(delete(self.model))

    async def count(self):
        result = await self.session.execute(select(func.count(self.model.id)))
        return result.scalar_one()

    async def commit(self):
        await self.session.commit()

    async def flush(self, *objects):
        await self.session.flush(objects)
