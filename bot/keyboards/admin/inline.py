from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Рассылка", callback_data="admin_spam")]
    ]
)
