from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload

from app.services.exceptions import NotFoundError
from app.services.schemas.analyzes import AnalysisSchema, AnalysisTypeSchema, AnalysisTypeWithAnalyzesSchema


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class AnalyzesAdapter:
    """Адаптер для доступа к данным анализов."""

    _session_factory: Callable[[], AbstractAsyncContextManager["AsyncSession"]]

    async def get_all(self, *, for_main: bool) -> list["AnalysisSchema"]:
        """Получить все активные анализы."""
        query = select(self._analysis).where(self._analysis.is_active.is_(True))

        if for_main:
            query = query.where(self._analysis.on_main.is_(True))

        async with self._session_factory() as session:
            rows = await session.execute(query)
            return [AnalysisSchema.model_validate(row) for row in rows.scalars()]

    async def get(self, id: int) -> "AnalysisSchema":
        """Получить анализ."""
        query = select(self._analysis).where(self._analysis.id == id, self._analysis.is_active.is_(True))

        async with self._session_factory() as session:
            row = await session.execute(query)

            try:
                analysis = AnalysisSchema.model_validate(row.one()[0])
            except NoResultFound as exc:
                message = f"Анализ с {id=} не найден."
                raise NotFoundError(message) from exc

        return analysis


class AnalysisTypeAdapter:
    """Адаптер для доступа к категориям анализов."""

    def __init__(self, session_factory: Callable[[], AbstractAsyncContextManager["AsyncSession"]]) -> None:
        self._session_factory = session_factory
        self._analysis_type = AnalysisType

    async def get_all(self) -> list["AnalysisTypeSchema"]:
        """Получить все категории анализов."""
        query = select(self._analysis_type)

        async with self._session_factory() as session:
            rows = await session.execute(query)
            return [AnalysisTypeSchema.model_validate(row) for row in rows.unique().scalars()]

    async def get(self, id: int) -> "AnalysisTypeWithAnalyzesSchema":
        """Получить категорию анализа."""
        query = (
            select(self._analysis_type)
            .options(joinedload(self._analysis_type.analyzes))
            .where(self._analysis_type.id == id)
        )

        async with self._session_factory() as session:
            row = await session.execute(query)

            try:
                analysis_type = AnalysisTypeWithAnalyzesSchema.model_validate(row.unique().one()[0])
            except NoResultFound as exc:
                message = f"Категория анализов с {id=} не найдена."
                raise NotFoundError(message) from exc

        return analysis_type
