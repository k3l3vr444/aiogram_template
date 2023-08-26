import logging

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.keyboards.admin import inline as admin_inline
from bot.models.state.admin import AdminSpam

logger = logging.getLogger(__name__)
admin_command_router = Router()


@admin_command_router.message(Command("admin"))
@admin_command_router.callback_query(AdminSpam(), F.data == 'cancel')
async def menu(message_or_callback: Message | CallbackQuery, state: FSMContext):
    await state.clear()
    if isinstance(message_or_callback, CallbackQuery):
        message = message_or_callback.message
    elif isinstance(message_or_callback, Message):
        message = message_or_callback
    else:
        raise ValueError
    await message.answer("Hello, admin!",
                         reply_markup=admin_inline.menu
                         )
