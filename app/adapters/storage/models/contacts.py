import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.adapters.storage.db.base_model import BaseModel
from fastapi_storages.integrations.sqlalchemy import FileType


from fastapi_storages import FileSystemStorage
from utils.constants import MEDIA_DIR


class City(BaseModel):
    """Города."""

    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(sa.BigInteger(), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(sa.String(30))
    is_active: Mapped[bool]

    offices: Mapped[list["Office"]] = relationship("Office", back_populates="city")

    def __str__(self) -> str:
        return self.name


class Office(BaseModel):
    """Филиалы."""

    __tablename__ = "offices"

    id: Mapped[int] = mapped_column(sa.BigInteger(), primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column(sa.String(100))
    address: Mapped[str] = mapped_column(sa.String(100))
    work_time: Mapped[str] = mapped_column(sa.String(100))
    phone: Mapped[str] = mapped_column(sa.String(20))
    email: Mapped[str] = mapped_column(sa.String(30))
    main_doctor: Mapped[str] = mapped_column(sa.String(50))
    main_doctor_work_time: Mapped[str] = mapped_column(sa.String(100))
    point_x: Mapped[str] = mapped_column(sa.String(10))
    point_y: Mapped[str] = mapped_column(sa.String(10))
    is_active: Mapped[bool]

    city_id: Mapped[int] = mapped_column(
        sa.BigInteger(), sa.ForeignKey("cities.id", ondelete="CASCADE")
    )

    city: Mapped["City"] = relationship("City", back_populates="offices")
    departments: Mapped["Department"] = relationship("Department", back_populates="office")

    def __str__(self) -> str:
        return self.address


class Department(BaseModel):
    """Отделения."""

    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(sa.BigInteger(), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(sa.String(100))
    tags: Mapped[str | None] = mapped_column(sa.String(100))
    short_description: Mapped[str] = mapped_column(sa.String(255))
    description: Mapped[str] = mapped_column(sa.String(255))
    photo: Mapped[str] = mapped_column(
        FileType(storage=FileSystemStorage(path=str(MEDIA_DIR / "departments")))
    )
    is_active: Mapped[bool]

    office_id: Mapped[int] = mapped_column(
        sa.BigInteger(), sa.ForeignKey("offices.id", ondelete="CASCADE")
    )

    office: Mapped["Office"] = relationship("Office", back_populates="departments")

    def __str__(self) -> str:
        return self.name
