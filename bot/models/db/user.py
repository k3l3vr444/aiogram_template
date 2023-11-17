from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from bot.models import dto
from bot.models.db.base import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[Optional[str]]
    full_name: Mapped[str]
    registration_time: Mapped[datetime] = mapped_column(default=datetime.now,
                                                        server_default=func.now())
    last_seen: Mapped[datetime] = mapped_column(default=datetime.now,
                                                server_default=func.now())
    is_active: Mapped[bool] = mapped_column(server_default='t')

    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self):
        return f"User [ID: {self.id}, Username: {self.username}, Fullname:{self.full_name}, " \
               f"Registration Time: {self.registration_time}, Last Seen: {self.last_seen}]"

    def to_dto(self) -> dto.User:
        return dto.User(id=self.id,
                        username=self.username,
                        full_name=self.full_name,
                        registration_time=self.registration_time,
                        last_seen=self.last_seen,
                        is_active=self.is_active)
