from aiogram.fsm.state import StatesGroup, State


class AdminSpam(StatesGroup):
    message = State()
