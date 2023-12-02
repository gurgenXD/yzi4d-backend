from datetime import datetime, timedelta

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app.adapters.storage.db.base_model import BaseModel


class Update(BaseModel):
    """Обновление."""

    __tablename__ = "updates"

    id: Mapped[int] = mapped_column(sa.BigInteger(), primary_key=True, autoincrement=True)
    start_update: Mapped[datetime]
    end_update: Mapped[datetime | None]
    status: Mapped[str] = mapped_column(sa.String(20))
    data_type: Mapped[str] = mapped_column(sa.String(20))
    error_log: Mapped[str | None] = mapped_column(sa.Text())

    @property
    def duration(self) -> timedelta | None:
        """Длительность обновления."""
        if self.end_update:
            return self.end_update - self.start_update
        return None

    def __str__(self) -> str:
        return self.status
