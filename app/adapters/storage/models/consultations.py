from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app.adapters.storage.db.base_model import BaseModel


class Consultation(BaseModel):
    """Онлайн-консультация."""

    __tablename__ = "consultations"

    id: Mapped[int] = mapped_column(sa.BigInteger(), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(sa.String(255))
    phone: Mapped[str] = mapped_column(sa.String(30))
    created: Mapped[datetime]
    specialist: Mapped[str] = mapped_column(sa.String(255))
    status: Mapped[str] = mapped_column(sa.String(20))
    comments: Mapped[str] = mapped_column(sa.Text())

    def __str__(self):
        return f"Онлайн консультация №: {self.id}"
