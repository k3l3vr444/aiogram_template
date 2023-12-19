import logging

from aiogram import Router, F
from aiogram.types import ChatMemberUpdated

from bot.models import dto
from bot.services.holder import ServiceHolder

my_chat_member_router = Router(name=__name__)

logger = logging.getLogger(__name__)


@my_chat_member_router.my_chat_member(F.chat.type == "private")
async def banned_by_user1(
    event: ChatMemberUpdated, service: ServiceHolder, user: dto.User
):
    if event.new_chat_member.status == "kicked":
        is_active = False
    elif event.new_chat_member.status == "member":
        is_active = True
    else:
        logger.error(f"New ChatMemberUpdated status {event.new_chat_member.status}")
        raise ValueError
    await service.account.update_user(user_id=user.id, is_active=is_active)
