from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass
from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.orm import contains_eager

from app.domain.entities.vacancies import VacancyCategoryEntity
from app.infrastructure.adapters.storage.models import Vacancy, VacancyCategory


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class VacanciesAdapter:
    """Адаптер для доступа к данным вакансий."""

    _session_factory: Callable[[], AbstractAsyncContextManager["AsyncSession"]]

    async def get_all(self) -> list["VacancyCategoryEntity"]:
        """Получить все активные вакансии."""
        query = (
            select(VacancyCategory)
            .join(Vacancy)
            .options(contains_eager(VacancyCategory.vacancies))
            .where(VacancyCategory.is_active.is_(True), Vacancy.is_active.is_(True))
        )

        async with self._session_factory() as session:
            rows = await session.execute(query)
            return [VacancyCategoryEntity.model_validate(row) for row in rows.unique().scalars()]
