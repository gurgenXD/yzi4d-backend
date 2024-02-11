from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.adapters.storage.db.base_model import BaseModel


class Callback(BaseModel):
    """Обратные звонки."""

    __tablename__ = "callbacks"

    id: Mapped[int] = mapped_column(sa.BigInteger(), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(sa.String(100))
    phone: Mapped[str] = mapped_column(sa.String(20))
    message: Mapped[str | None] = mapped_column(sa.Text())
    created: Mapped[datetime]
    answered: Mapped[bool]
    call_back_time: Mapped[str | None]
