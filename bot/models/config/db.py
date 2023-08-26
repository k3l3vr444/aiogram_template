from dataclasses import dataclass


@dataclass
class DBConfig:
    host: str
    password: str
    user: str
    database: str
    echo: bool

    @property
    def uri(self):
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:5432/{self.database}"