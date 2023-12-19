from dataclasses import dataclass
from pathlib import Path
from typing import Self

import yaml

from bot.models.config.bot import BotConfig
from bot.models.config.db import DBConfig
from bot.models.config.path import Paths


@dataclass
class Config:
    bot: BotConfig
    db: DBConfig
    paths: Paths

    @classmethod
    def load(cls, root_path: Path) -> Self:
        paths = Paths(root_path)
        with paths.config.open("r", encoding="utf8") as f:
            config_dct = yaml.safe_load(f)
        return Config(
            bot=BotConfig.load_from_dict(config_dct["bot"]),
            db=DBConfig.load_from_dict(config_dct["db"]),
            paths=paths,
        )
