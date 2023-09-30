from datetime import date

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app.adapters.storage.db.base_model import BaseModel
from fastapi_storages.integrations.sqlalchemy import FileType


from fastapi_storages import FileSystemStorage
from utils.constants import MEDIA_DIR


class Promotion(BaseModel):
    """Акции."""

    __tablename__ = "promotions"

    id: Mapped[int] = mapped_column(sa.BigInteger(), primary_key=True, autoincrement=True)
    guid: Mapped[str] = mapped_column(sa.String(36), unique=True)
    name: Mapped[str] = mapped_column(sa.String(100))
    sale: Mapped[str] = mapped_column(sa.String(100))
    description: Mapped[str | None] = mapped_column(sa.Text())
    photo: Mapped[str] = mapped_column(FileType(storage=FileSystemStorage(path=str(MEDIA_DIR / "promotions"))))
    date_start: Mapped[date]
    date_end: Mapped[date]
    on_main: Mapped[bool]
