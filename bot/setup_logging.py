import logging.config
import os
from datetime import datetime

import yaml
from sqlalchemy import log as sqlalchemy_log

from bot.models.config.config import Config

logger = logging.getLogger(__name__)


class FileRotateNameHandler(logging.FileHandler):
    def __init__(self, mode='a', encoding=None, delay=False, errors=None):
        try:
            os.mkdir('logs')
        except FileExistsError:
            pass
        super().__init__(f"logs/{datetime.now().strftime('%Y_%m_%d-%H_%M')}.log",
                         mode=mode, encoding=encoding, delay=delay, errors=errors)


def setup_logging(config: Config):
    if config.db.echo:
        sqlalchemy_log._add_default_handler = lambda x: None
    try:
        with config.paths.logging.open("r") as f:
            logging_config = yaml.safe_load(f)
        if 'file_handler' not in logging_config['root']['handlers']:
            del logging_config['handlers']['file_handler']

        logging.config.dictConfig(logging_config)
        logger.info("Logging configured successfully")
    except IOError:
        logging.basicConfig(level=logging.DEBUG)
        logger.warning("Logging config file not found, use basic config")
