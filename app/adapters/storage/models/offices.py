from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.adapters.storage.db.base_model import BaseModel


if TYPE_CHECKING:
    from app.adapters.storage.models.departments import Department


class Office(BaseModel):
    """Филиалы."""

    __tablename__ = "offices"

    city_id: Mapped[int] = mapped_column(sa.BigInteger(), sa.ForeignKey("cities.id"))
    description: Mapped[str] = mapped_column(sa.String(100))
    address: Mapped[str] = mapped_column(sa.String(100))
    work_time: Mapped[str] = mapped_column(sa.String(100))
    phone: Mapped[str] = mapped_column(sa.String(20))
    email: Mapped[str] = mapped_column(sa.String(30))
    main_doctor: Mapped[str] = mapped_column(sa.String(50))
    main_doctor_work_time: Mapped[str] = mapped_column(sa.String(50))
    coor_x: Mapped[str] = mapped_column(sa.String(10))
    coor_y: Mapped[str] = mapped_column(sa.String(10))

    city: Mapped["City"] = relationship("City", back_populates="offices")
    departments: Mapped["Department"] = relationship("Department", back_populates="office")

    def __str__(self) -> str:
        return self.address


class City(BaseModel):
    """Города."""

    __tablename__ = "cities"

    name: Mapped[str] = mapped_column(sa.String(30))

    offices: Mapped[list["Office"]] = relationship("Office", back_populates="city")

    def __str__(self) -> str:
        return self.name
