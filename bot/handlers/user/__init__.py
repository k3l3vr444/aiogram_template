from aiogram import Router

from . import account

user_router = Router()
user_router.include_routers(account.router)
