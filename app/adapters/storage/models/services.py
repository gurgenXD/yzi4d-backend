import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.adapters.storage.db.base_model import BaseModel


class ServiceType(BaseModel):
    """Тип услуг."""

    __tablename__ = "services_types"

    id: Mapped[str] = mapped_column(sa.String(36), primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(30))
    on_main: Mapped[bool]
    is_active: Mapped[bool]

    def __str__(self) -> str:
        return self.name


class Service(BaseModel):
    """Услуги."""

    __tablename__ = "services"

    id: Mapped[str] = mapped_column(sa.String(36), primary_key=True)
    parent_id: Mapped[str | None] = mapped_column(sa.String(36), sa.ForeignKey("services.id"))
    name: Mapped[str] = mapped_column(sa.String(100))
    short_description: Mapped[str | None] = mapped_column(sa.String(300))
    description: Mapped[str | None] = mapped_column(sa.Text())
    is_group: Mapped[bool]
    is_active: Mapped[bool]
    on_main: Mapped[bool]

    parent = relationship("Service", remote_side=[id])

    def __str__(self) -> str:
        return self.name
