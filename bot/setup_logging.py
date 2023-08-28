import logging.config
import os
from datetime import datetime

import yaml

from bot.models.config.config import Config

logger = logging.getLogger(__name__)


def prepare_file_handler(logging_config: dict):
    if 'file_handler' in logging_config['root']['handlers']:
        try:
            os.mkdir("logs")
        except FileExistsError:
            pass
        logging_config['handlers']['file_handler']['filename'] = f"logs/{datetime.now().strftime('%Y_%m_%d-%H_%M')}.log"


def setup_logging(config: Config):
    try:
        with config.paths.logging.open("r") as f:
            logging_config = yaml.safe_load(f)
        prepare_file_handler(logging_config)
        logging.config.dictConfig(logging_config)
        logger.info("Logging configured successfully")
    except IOError:
        logging.basicConfig(level=logging.DEBUG)
        logger.warning("Logging config file not found, use basic config")
