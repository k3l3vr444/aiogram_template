from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class TemplateCallbackData(CallbackData, prefix="prefix"):
    id: int


def template_keyboard() -> InlineKeyboardMarkup:
    keyboard = []
    button_row = []
    # Factory
    button = InlineKeyboardButton(
        text="text", callback_data=TemplateCallbackData(id=1).pack()
    )
    button_row.append(button)
    # HardCode
    button = InlineKeyboardButton(text="text", callback_data="callback")
    button_row.append(button)

    keyboard.append(button_row)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def cancel(back: bool = False):
    inline_keyboard = [
        [InlineKeyboardButton(text="Отмена", callback_data="cancel")],
    ]
    if back:
        inline_keyboard.append(
            [InlineKeyboardButton(text="Назад", callback_data="back")]
        )
    keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return keyboard
