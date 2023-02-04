from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app.adapters.storage.db.base_model import BaseModel


class Promotion(BaseModel):
    """Акции."""

    __tablename__ = "promotions"

    sale: Mapped[str] = mapped_column(sa.String(30))
    title: Mapped[str] = mapped_column(sa.String(20))
    description: Mapped[str] = mapped_column(sa.String(100))
    photo: Mapped[str | None] = mapped_column(sa.String(150))
    services: Mapped[str] = mapped_column(sa.String(100))
    date_start: Mapped[datetime]
    date_end: Mapped[datetime]
    url: Mapped[str] = mapped_column(sa.String(100))
    is_active: Mapped[bool] = mapped_column(default=False)
    on_main: Mapped[bool] = mapped_column(default=False)
