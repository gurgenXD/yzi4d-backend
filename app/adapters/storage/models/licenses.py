import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app.adapters.storage.db.base_model import BaseModel


class License(BaseModel):
    """Лизцензии."""

    __tablename__ = "licenses"

    id: Mapped[int] = mapped_column(sa.BigInteger(), primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(sa.String(50))
    document: Mapped[str | None] = mapped_column(sa.String(150))
    is_active: Mapped[bool]
