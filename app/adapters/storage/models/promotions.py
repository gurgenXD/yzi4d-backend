from datetime import date

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app.adapters.storage.db.base_model import BaseModel


class Promotion(BaseModel):
    """Акции."""

    __tablename__ = "promotions"

    name: Mapped[str] = mapped_column(sa.String(30))
    sale: Mapped[str] = mapped_column(sa.String(30))
    description: Mapped[str] = mapped_column(sa.String(500))
    photo: Mapped[str] = mapped_column(sa.String(150))
    date_start: Mapped[date]
    date_end: Mapped[date]
    on_main: Mapped[bool] = mapped_column(default=False)
