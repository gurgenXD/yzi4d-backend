import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.adapters.storage.db.base_model import BaseModel


class Page(BaseModel):
    """Статические страницы."""

    __tablename__ = "pages"

    id: Mapped[int] = mapped_column(sa.BigInteger(), primary_key=True, autoincrement=True)
    url: Mapped[str] = mapped_column(sa.String(100), unique=True)
    title: Mapped[str] = mapped_column(sa.String(100))
    content: Mapped[str] = mapped_column(sa.Text())
    is_active: Mapped[bool]
