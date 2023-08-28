from dataclasses import dataclass

from bot.models.config.bot import BotConfig
from bot.models.config.db import DBConfig
from bot.models.config.path import Paths


@dataclass
class Config:
    bot: BotConfig
    db: DBConfig
    paths: Paths
