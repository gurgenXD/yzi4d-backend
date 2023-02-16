from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app.adapters.storage.db.base_model import BaseModel


class News(BaseModel):
    """Новости."""

    __tablename__ = "news"

    title: Mapped[str] = mapped_column(sa.String(50))
    preview: Mapped[str] = mapped_column(sa.String(150))
    created: Mapped[datetime] = mapped_column(default=datetime.now)
    description: Mapped[str] = mapped_column(sa.String(500))
    photo: Mapped[str | None] = mapped_column(sa.String(150))
    is_active: Mapped[bool] = mapped_column(default=False)
