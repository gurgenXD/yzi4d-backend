import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app.adapters.storage.db.base_model import BaseModel


class Page(BaseModel):
    """Статические страницы."""

    __tablename__ = "pages"

    slug: Mapped[str] = mapped_column(sa.String(100), unique=True)
    title: Mapped[str] = mapped_column(sa.String(20))
    body: Mapped[str] = mapped_column(sa.Text())
    is_active: Mapped[bool] = mapped_column(default=False)
