from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📱 Ваш кабинет")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
