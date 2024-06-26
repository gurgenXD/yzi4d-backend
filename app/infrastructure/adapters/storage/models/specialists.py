from datetime import date
from typing import TYPE_CHECKING, Any

import sqlalchemy as sa
from fastapi_storages import FileSystemStorage
from fastapi_storages.integrations.sqlalchemy import FileType
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.adapters.storage.db.base_model import BaseModel
from utils.constants import MEDIA_DIR


if TYPE_CHECKING:
    from app.infrastructure.adapters.storage.models.services import Service


specializations_specialists_table = sa.Table(
    "specializations_specialists_rel",
    BaseModel.metadata,
    sa.Column("specialization_id", sa.ForeignKey("specializations.id", ondelete="CASCADE"), primary_key=True),
    sa.Column("specialist_id", sa.ForeignKey("specialists.id", ondelete="CASCADE"), primary_key=True),
)


class Specialization(BaseModel):
    """Специальность."""

    __tablename__ = "specializations"

    id: Mapped[int] = mapped_column(sa.BigInteger(), primary_key=True, autoincrement=True)
    guid: Mapped[str] = mapped_column(sa.String(36), unique=True)
    name: Mapped[str] = mapped_column(sa.String(50))
    is_active: Mapped[bool]

    specialists: Mapped[list["Specialist"]] = relationship(
        "Specialist", secondary=specializations_specialists_table, back_populates="specializations"
    )

    def __str__(self) -> str:
        return self.name


class Specialist(BaseModel):
    """Специалист."""

    __tablename__ = "specialists"

    id: Mapped[int] = mapped_column(sa.BigInteger(), primary_key=True, autoincrement=True)
    guid: Mapped[str] = mapped_column(sa.String(36), unique=True)
    name: Mapped[str] = mapped_column(sa.String(50))
    surname: Mapped[str] = mapped_column(sa.String(50))
    patronymic: Mapped[str | None] = mapped_column(sa.String(50))
    photo: Mapped[str | None] = mapped_column(FileType(storage=FileSystemStorage(path=str(MEDIA_DIR / "specialists"))))
    start_work_date: Mapped[date]
    education: Mapped[list[dict[str, Any]] | None] = mapped_column(sa.JSON())
    activity: Mapped[list[dict[str, Any]] | None] = mapped_column(sa.JSON())
    titles: Mapped[list[dict[str, Any]] | None] = mapped_column(sa.JSON())
    description: Mapped[str | None] = mapped_column(sa.Text())
    short_description: Mapped[str | None] = mapped_column(sa.String(250))
    seo_description: Mapped[str | None] = mapped_column(sa.Text())
    can_adult: Mapped[bool]
    can_child: Mapped[bool]
    can_online: Mapped[bool]
    on_main: Mapped[bool]
    is_active: Mapped[bool]

    specializations: Mapped[list["Specialization"]] = relationship(
        "Specialization", secondary=specializations_specialists_table, back_populates="specialists"
    )
    certificates: Mapped[list["Certificate"]] = relationship("Certificate", back_populates="specialist")

    def __str__(self) -> str:
        patronymic = f" {self.patronymic}" if self.patronymic else ""
        return f"{self.surname} {self.name}" + patronymic


class Certificate(BaseModel):
    """Сертификаты специалиста."""

    __tablename__ = "certificates"

    id: Mapped[int] = mapped_column(sa.BigInteger(), primary_key=True, autoincrement=True)
    guid: Mapped[str] = mapped_column(sa.String(36), unique=True)
    name: Mapped[str] = mapped_column(sa.String(250))
    file: Mapped[str] = mapped_column(FileType(storage=FileSystemStorage(path=str(MEDIA_DIR / "certificates"))))

    specialist_id: Mapped[int] = mapped_column(sa.BigInteger(), sa.ForeignKey("specialists.id", ondelete="CASCADE"))

    specialist: Mapped["Specialist"] = relationship("Specialist", back_populates="certificates")

    def __str__(self) -> str:
        return self.name


class SpecialistService(BaseModel):
    """Услуга специалиста."""

    __tablename__ = "specialists_services"

    price: Mapped[int]
    is_active: Mapped[bool]

    service_id: Mapped[int] = mapped_column(
        sa.BigInteger(), sa.ForeignKey("services.id", ondelete="CASCADE"), primary_key=True
    )
    specialist_id: Mapped[int] = mapped_column(
        sa.BigInteger(), sa.ForeignKey("specialists.id", ondelete="CASCADE"), primary_key=True
    )

    service: Mapped["Service"] = relationship("Service", back_populates="specialists_services")
