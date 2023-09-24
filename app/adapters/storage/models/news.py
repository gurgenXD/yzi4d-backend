from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app.adapters.storage.db.base_model import BaseModel
from fastapi_storages.integrations.sqlalchemy import FileType


from fastapi_storages import FileSystemStorage
from utils.constants import MEDIA_DIR


class News(BaseModel):
    """Новости."""

    __tablename__ = "news"

    id: Mapped[int] = mapped_column(sa.BigInteger(), primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(sa.String(50))
    preview: Mapped[str] = mapped_column(sa.String(150))
    created: Mapped[datetime]
    description: Mapped[str] = mapped_column(sa.String(500))
    photo: Mapped[str | None] = mapped_column(
        FileType(storage=FileSystemStorage(path=str(MEDIA_DIR / "news")))
    )
    is_active: Mapped[bool]
