from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from app.adapters.storage.models import Analysis
from app.services.exceptions import NotFoundError
from app.services.schemas.analyzes import AnalysisSchema

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class AnalyzesAdapter:
    """Адаптер для доступа к данным анализов."""

    def __init__(
        self, session_factory: Callable[[], AbstractAsyncContextManager["AsyncSession"]]
    ) -> None:
        self._session_factory = session_factory
        self._analysis = Analysis

    async def get_all(self, *, for_main: bool) -> list["AnalysisSchema"]:
        """Получить все активные анализы."""
        query = select(self._analysis).where(self._analysis.is_active.is_(True))

        if for_main:
            query = query.where(self._analysis.on_main.is_(True))

        async with self._session_factory() as session:
            rows = await session.execute(query)
            return [AnalysisSchema.from_orm(row) for row in rows.scalars()]

    async def get(self, id: int) -> "AnalysisSchema":
        """Получить анализ."""
        query = select(self._analysis).where(
            self._analysis.id == id, self._analysis.is_active.is_(True)
        )

        async with self._session_factory() as session:
            row = await session.execute(query)

            try:
                analysis = AnalysisSchema.from_orm(row.one()[0])
            except NoResultFound as exc:
                message = f"Анализ с {id=} не найден."
                raise NotFoundError(message) from exc

        return analysis
