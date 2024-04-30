import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.adapters.storage.db.base_model import BaseModel


class VacancyCategory(BaseModel):
    """Категория вакансии."""

    __tablename__ = "vacancies_categories"

    id: Mapped[int] = mapped_column(sa.BigInteger(), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(sa.String(255))
    position: Mapped[int]
    is_active: Mapped[bool]

    vacancies: Mapped[list["Vacancy"]] = relationship("Vacancy", back_populates="category")

    def __str__(self) -> str:
        return self.name


class Vacancy(BaseModel):
    """Вакансия."""

    __tablename__ = "vacancies"

    id: Mapped[int] = mapped_column(sa.BigInteger(), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(sa.String(255))
    is_active: Mapped[bool]

    category_id: Mapped[str] = mapped_column(
        sa.BigInteger(), sa.ForeignKey("vacancies_categories.id", ondelete="CASCADE")
    )

    category: Mapped["VacancyCategory"] = relationship("VacancyCategory", back_populates="vacancies")

    def __str__(self) -> str:
        return self.name
