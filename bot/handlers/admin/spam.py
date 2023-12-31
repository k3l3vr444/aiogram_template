import asyncio
import logging
from datetime import datetime

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.keyboards import inline
from bot.models.config import Config
from bot.models.state.admin import AdminSpam
from bot.services.holder import ServiceHolder

logger = logging.getLogger(__name__)
router = Router()


@router.callback_query(F.data == "admin_spam")
async def spam_button(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AdminSpam.message)
    await callback.message.answer(
        "Введите текст рассылки", reply_markup=inline.cancel()
    )


@router.message(AdminSpam.message)
async def input_message(
    message: Message, state: FSMContext, service: ServiceHolder, config: Config
):
    await state.clear()
    logger.warning(f"Starting spamming users with message: {message.text}")
    tmp_time = datetime.now()
    async for user in service.account.paginate_users():
        if user.id in config.bot.admin_ids:
            logger.info(f"Spam skipped admin {user.id}")
            continue
        try:
            await message.bot.send_message(chat_id=user.id, text=message.text)
        except Exception as e:
            logger.error(f"Error while sending spam, target: {user.id}|{e}")
        await asyncio.sleep(0.3)
    logger.info(f"Spam finished, timedelta: {datetime.now() - tmp_time}")
    await message.answer(f"Рассылка завершена успешно")
