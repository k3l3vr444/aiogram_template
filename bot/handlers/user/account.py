import logging

from aiogram import Router, F
from aiogram.types import Message

from bot.models.dto import User

logger = logging.getLogger(__name__)
router = Router()


@router.message(F.text == "📱 Ваш кабинет")
async def account_button(message: Message, user: User):
    await message.answer(
        f"📱 Ваш кабинет:\n" f"➖➖➖➖➖➖➖➖➖\n" f"🆔 Мой ID: {user.id}\n" f"➖➖➖➖➖➖➖➖➖"
    )
