from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.adapters.storage.db.base_model import BaseModel


if TYPE_CHECKING:
    from app.adapters.storage.models.offices import Office


class Department(BaseModel):
    """Отделения."""

    __tablename__ = "departments"

    office_id: Mapped[int] = mapped_column(sa.BigInteger(), sa.ForeignKey("offices.id"))
    name: Mapped[str] = mapped_column(sa.String(100))
    tags: Mapped[str | None] = mapped_column(sa.String(100))
    short_description: Mapped[str] = mapped_column(sa.String(300))
    description: Mapped[str] = mapped_column(sa.Text())
    photo: Mapped[str | None] = mapped_column(sa.String(150))
    is_active: Mapped[bool] = mapped_column(default=False)

    office: Mapped["Office"] = relationship("Office", back_populates="departments")

    def __str__(self) -> str:
        return self.name
