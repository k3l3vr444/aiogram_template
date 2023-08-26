from aiogram.filters import Filter
from aiogram.types import Message


class AdminFilter(Filter):
    def __init__(self, superusers: list[int]) -> None:
        self.superusers = superusers

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.superusers
