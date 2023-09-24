from datetime import date

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app.adapters.storage.db.base_model import BaseModel


class Promotion(BaseModel):
    """Акции."""

    __tablename__ = "promotions"

    id: Mapped[int] = mapped_column(sa.BigInteger(), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(sa.String(100))
    sale: Mapped[str] = mapped_column(sa.String(30))
    description: Mapped[str | None] = mapped_column(sa.Text())
    photo: Mapped[str] = mapped_column(sa.String(150))
    date_start: Mapped[date]
    date_end: Mapped[date]
    on_main: Mapped[bool]
