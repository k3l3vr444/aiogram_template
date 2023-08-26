from bot.dao import UserDAO
from bot.services.user import select_user


async def user_id(user_dao: UserDAO, text: str) -> int:
    user_id_ = int(text)
    await select_user(user_dao=user_dao, user_id=user_id_)
    return user_id_
