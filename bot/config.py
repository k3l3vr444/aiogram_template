from pathlib import Path

import yaml

from bot.models.config.bot import BotConfig
from bot.models.config.config import Config
from bot.models.config.db import DBConfig
from bot.models.config.path import Paths


def load_bot_config(dct: dict) -> BotConfig:
    return BotConfig(
        token=dct["token"],
        admin_id=dct["admin_id"],
        use_redis=dct["use_redis"],
        error_handler_id=dct["error_handler_id"]
    )


def load_db_config(dct: dict) -> DBConfig:
    return DBConfig(
        host=dct["host"],
        password=dct["password"],
        user=dct["user"],
        database=dct["database"],
        echo=dct["echo"]
    )


def load_config(root_path: Path) -> Config:
    paths = Paths(root_path)
    with paths.config.open("r", encoding="utf8") as f:
        config_dct = yaml.safe_load(f)
    return Config(
        bot=load_bot_config(config_dct['bot']),
        db=load_db_config(config_dct['db']),
        paths=paths
    )
