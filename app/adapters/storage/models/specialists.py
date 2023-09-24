from datetime import date

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.adapters.storage.db.base_model import BaseModel
from fastapi_storages.integrations.sqlalchemy import FileType


from fastapi_storages import FileSystemStorage
from utils.constants import MEDIA_DIR


specializations_specialists_table = sa.Table(
    "specializations_specialists_rel",
    BaseModel.metadata,
    sa.Column(
        "specialization_id",
        sa.ForeignKey("specializations.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    sa.Column(
        "specialist_id", sa.ForeignKey("specialists.id", ondelete="CASCADE"), primary_key=True
    ),
)


class Specialization(BaseModel):
    """Специальность."""

    __tablename__ = "specializations"

    id: Mapped[str] = mapped_column(sa.String(36), primary_key=True)
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

    id: Mapped[str] = mapped_column(sa.String(36), primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(50))
    surname: Mapped[str] = mapped_column(sa.String(50))
    patronymic: Mapped[str | None] = mapped_column(sa.String(50))
    photo: Mapped[str | None] = mapped_column(
        FileType(storage=FileSystemStorage(path=str(MEDIA_DIR / "specialists")))
    )
    start_work_date: Mapped[date]
    education: Mapped[str | None] = mapped_column(sa.Text())
    activity: Mapped[str | None] = mapped_column(sa.Text())
    description: Mapped[str | None] = mapped_column(sa.Text())
    titles: Mapped[str | None] = mapped_column(sa.Text())
    can_adult: Mapped[bool]
    can_child: Mapped[bool]
    can_online: Mapped[bool]
    on_main: Mapped[bool]
    is_active: Mapped[bool]

    specializations: Mapped[list["Specialization"]] = relationship(
        "Specialization", secondary=specializations_specialists_table, back_populates="specialists"
    )
    certificates: Mapped[list["SpecialistCertificate"]] = relationship(
        "SpecialistCertificate", back_populates="specialist"
    )

    def __str__(self) -> str:
        patronymic = f" {self.patronymic}" if self.patronymic else ""
        return f"{self.surname} {self.name}" + patronymic


class SpecialistCertificate(BaseModel):
    """Сертификаты специалиста."""

    __tablename__ = "specialist_certificates"

    id: Mapped[str] = mapped_column(sa.String(36), primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(250))
    file: Mapped[str] = mapped_column(
        FileType(storage=FileSystemStorage(path=str(MEDIA_DIR / "certificates")))
    )

    specialist_id: Mapped[str] = mapped_column(
        sa.String(36), sa.ForeignKey("specialists.id", ondelete="CASCADE")
    )

    specialist: Mapped["Specialist"] = relationship("Specialist", back_populates="certificates")

    def __str__(self) -> str:
        return self.name
