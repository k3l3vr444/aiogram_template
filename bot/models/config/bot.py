from dataclasses import dataclass


@dataclass
class BotConfig:
    token: str
    admin_id: list[int]
    use_redis: bool
    error_handler_id: list[int]
