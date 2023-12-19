from pathlib import Path

from bot.models.config import Config

config = Config.load(Path(__file__).parent.parent)
