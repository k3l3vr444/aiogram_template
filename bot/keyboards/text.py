from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def template_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="text")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
