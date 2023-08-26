from aiogram import Router

from . import spam

admin_router = Router()
admin_router.include_routers(spam.router)
