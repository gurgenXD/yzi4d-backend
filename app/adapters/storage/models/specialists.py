from datetime import date

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.adapters.storage.db.base_model import BaseModel

specializations_specialists_table = sa.Table(
    "specializations_specialists",
    BaseModel.metadata,
    sa.Column("specialization_id", sa.ForeignKey("specializations.id"), primary_key=True),
    sa.Column("specialist_id", sa.ForeignKey("specialists.id"), primary_key=True),
)


class Specialization(BaseModel):
    """Специальность."""

    __tablename__ = "specializations"

    name: Mapped[str] = mapped_column(sa.String(30))

    specialists: Mapped[set["Specialist"]] = relationship(
        "Specialist", secondary=specializations_specialists_table, back_populates="specializations"
    )

    def __str__(self) -> str:
        return self.name


class Specialist(BaseModel):
    """Специалист."""

    __tablename__ = "specialists"

    name: Mapped[str] = mapped_column(sa.String(50))
    surname: Mapped[str] = mapped_column(sa.String(50))
    patronymic: Mapped[str] = mapped_column(sa.String(50))
    photo: Mapped[str | None] = mapped_column(sa.String(150))
    start_work_date: Mapped[date]
    description: Mapped[str | None] = mapped_column(sa.Text())
    titles: Mapped[str | None] = mapped_column(sa.Text())
    on_main: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=False)

    specializations: Mapped[set["Specialization"]] = relationship(
        "Specialization", secondary=specializations_specialists_table, back_populates="specialists"
    )

    def __str__(self) -> str:
        return self.full_name

    @property
    def full_name(self) -> str:
        """Полное имя."""
        name = f"{self.surname} {self.name}"

        if self.patronymic:
            name = f"{name} {self.patronymic}"

        return name
