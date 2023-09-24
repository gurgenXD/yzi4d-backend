from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app.adapters.storage.db.base_model import BaseModel


class Updater(BaseModel):
    """Обновление."""

    __tablename__ = "updates"

    id: Mapped[int] = mapped_column(sa.BigInteger(), primary_key=True, autoincrement=True)
    start_update: Mapped[datetime]
    end_update: Mapped[datetime | None]
    status: Mapped[str] = mapped_column(sa.String(20))
    error_log: Mapped[str | None] = mapped_column(sa.Text())

    def __str__(self) -> str:
        return self.status
