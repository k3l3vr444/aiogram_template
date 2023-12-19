from dataclasses import dataclass
from typing import Self


@dataclass
class BotConfig:
    token: str
    admin_ids: list[int]
    use_redis: bool
    error_handler_id: list[int]

    @classmethod
    def load_from_dict(cls, dct: dict) -> Self:
        return cls(
            token=dct["token"],
            admin_ids=dct["admin_ids"],
            use_redis=dct["use_redis"],
            error_handler_id=dct["error_handler_id"],
        )
