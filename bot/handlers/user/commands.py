import logging

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.keyboards.user import text

logger = logging.getLogger(__name__)
user_command_router = Router()


@user_command_router.message(CommandStart())
async def menu(message_or_callback: Message | CallbackQuery, state: FSMContext):
    await state.clear()
    if isinstance(message_or_callback, CallbackQuery):
        message = message_or_callback.message
    elif isinstance(message_or_callback, Message):
        message = message_or_callback
    else:
        raise ValueError
    await message.answer('<b>Hello</> <i>user</>',
                         reply_markup=text.menu)
