from dataclasses import dataclass, field

from bot.dao import HolderDAO
from bot.services.account import AccountService


@dataclass
class ServiceHolder:
    dao: HolderDAO
    account: AccountService = field(init=False)

    def __post_init__(self):
        self.account = AccountService(self.dao)
