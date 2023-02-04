from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app.adapters.storage.db.base_model import BaseModel


class Callback(BaseModel):
    """Обратные звонки."""

    __tablename__ = "callbacks"

    name: Mapped[str] = mapped_column(sa.String(100))
    phone: Mapped[str] = mapped_column(sa.String(20))
    message: Mapped[str | None] = mapped_column(sa.Text())
    created: Mapped[datetime] = mapped_column(default=datetime.now)
    answered: Mapped[bool] = mapped_column(default=False)
    call_back_time: Mapped[str | None]
