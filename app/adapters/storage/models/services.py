import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.adapters.storage.db.base_model import BaseModel


class ServiceType(BaseModel):
    """Тип услуг."""

    __tablename__ = "services_types"

    name: Mapped[str] = mapped_column(sa.String(30))
    on_main: Mapped[bool] = mapped_column(default=False)

    services: Mapped[set["ServiceType"]] = relationship("Service", back_populates="service_type")

    def __str__(self) -> str:
        return self.name


class Service(BaseModel):
    """Услуги."""

    __tablename__ = "services"

    service_type_id: Mapped[int] = mapped_column(
        sa.BigInteger(), sa.ForeignKey("services_types.id")
    )
    name: Mapped[str] = mapped_column(sa.String(30))
    is_active: Mapped[bool] = mapped_column(default=False)
    on_main: Mapped[bool] = mapped_column(default=False)

    service_type: Mapped["Service"] = relationship("ServiceType", back_populates="services")

    def __str__(self) -> str:
        return self.name
