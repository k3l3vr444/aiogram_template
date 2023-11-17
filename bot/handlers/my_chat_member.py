import logging

from aiogram import Router
from aiogram.types import ChatMemberUpdated

from bot.dao.holder import HolderDAO
from bot.models import dto
from bot.services.user import update_user

my_chat_member_router = Router(name=__name__)

logger = logging.getLogger(__name__)


@my_chat_member_router.my_chat_member()
async def banned_by_user1(event: ChatMemberUpdated, dao: HolderDAO, user: dto.User):
    if event.new_chat_member.status == 'kicked':
        is_active = False
    elif event.new_chat_member.status == 'member':
        is_active = True
    else:
        logger.error(f'New ChatMemberUpdated status {event.new_chat_member.status}')
        raise ValueError
    await update_user(user_dao=dao.user,
                      user_id=user.id,
                      is_active=is_active)
