from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    id: int
    username: Optional[str]
    full_name: str
    registration_time: datetime
    last_seen: datetime
