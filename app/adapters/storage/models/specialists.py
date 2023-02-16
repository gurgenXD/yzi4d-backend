from datetime import date

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.adapters.storage.db.base_model import BaseModel


specializations_specialists_table = sa.Table(
    "specializations_specialists",
    BaseModel.metadata,
    sa.Column("specialization_id", sa.ForeignKey("specializations.id"), primary_key=True),
    sa.Column(
        "specialist_id", sa.ForeignKey("specialists.id", ondelete="CASCADE"), primary_key=True
    ),
)


class Specialization(BaseModel):
    """Специальность."""

    __tablename__ = "specializations"

    name: Mapped[str] = mapped_column(sa.String(30))

    specialists: Mapped[list["Specialist"]] = relationship(
        "Specialist", secondary=specializations_specialists_table, back_populates="specializations"
    )

    def __str__(self) -> str:
        return self.name


class Specialist(BaseModel):
    """Специалист."""

    __tablename__ = "specialists"

    guid_1c: Mapped[str] = mapped_column(sa.String(32))
    name: Mapped[str] = mapped_column(sa.String(50))
    surname: Mapped[str] = mapped_column(sa.String(50))
    patronymic: Mapped[str | None] = mapped_column(sa.String(50))
    photo: Mapped[str | None] = mapped_column(sa.String(150))
    start_work_date: Mapped[date]
    education: Mapped[str] = mapped_column(sa.Text())
    activity: Mapped[str | None] = mapped_column(sa.Text())
    description: Mapped[str | None] = mapped_column(sa.Text())
    titles: Mapped[str | None] = mapped_column(sa.Text())
    on_main: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=False)
    can_online: Mapped[bool] = mapped_column(default=False)

    specializations: Mapped[list["Specialization"]] = relationship(
        "Specialization", secondary=specializations_specialists_table, back_populates="specialists"
    )
    certificates: Mapped[list["SpecialistCertificate"]] = relationship(
        "SpecialistCertificate", back_populates="specialist"
    )

    def __str__(self) -> str:
        return f"{self.name} {self.surname}"


class SpecialistCertificate(BaseModel):
    """Сертификаты специалиста."""

    __tablename__ = "specialist_certificates"

    specialist_id: Mapped[int] = mapped_column(
        sa.BigInteger(), sa.ForeignKey("specialists.id", ondelete="CASCADE")
    )
    name: Mapped[str] = mapped_column(sa.String(250))
    path: Mapped[str] = mapped_column(sa.String(150))

    specialist: Mapped["Specialist"] = relationship("Specialist", back_populates="certificates")

    def __str__(self) -> str:
        return self.name
