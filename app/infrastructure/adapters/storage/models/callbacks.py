from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.adapters.storage.db.base_model import BaseModel


class Callback(BaseModel):
    """Обратные звонки."""

    __tablename__ = "callbacks"

    id: Mapped[int] = mapped_column(sa.BigInteger(), primary_key=True, autoincrement=True)
    phone: Mapped[str] = mapped_column(sa.String(20))
    created: Mapped[datetime]
    answered: Mapped[bool]
