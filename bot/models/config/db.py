from dataclasses import dataclass
from typing import Self


@dataclass
class DBConfig:
    host: str
    password: str
    user: str
    database: str
    echo: bool

    @classmethod
    def load_from_dict(cls, dct: dict) -> Self:
        return DBConfig(
            host=dct["host"],
            password=dct["password"],
            user=dct["user"],
            database=dct["database"],
            echo=dct["echo"],
        )

    @property
    def uri(self):
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:5432/{self.database}"
