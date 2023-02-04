from datetime import date

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app.adapters.storage.db.base_model import BaseModel


class User(BaseModel):
    """Пользователи."""

    __tablename__ = "users"

    username: Mapped[str] = mapped_column(sa.String(64), unique=True)
    email: Mapped[str] = mapped_column(sa.String(64), unique=True)
    password: Mapped[str] = mapped_column(sa.String(32))
    created: Mapped[date] = mapped_column(default=date.today)
    is_active: Mapped[bool] = mapped_column(default=False)
