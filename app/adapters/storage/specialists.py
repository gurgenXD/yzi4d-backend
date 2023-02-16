from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from typing import TYPE_CHECKING

from sqlalchemy import select, insert
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload

from app.adapters.storage.models import Specialist, Specialization
from app.services.exceptions import NotFoundError
from app.services.schemas.specialists import SpecialistSchema, SpecializationSchema

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from app.adapters.source import SourceSpecialistSchema


class SpecialistsAdapter:
    """Адаптер для доступа к данным специалистов."""

    def __init__(
        self, session_factory: Callable[[], AbstractAsyncContextManager["AsyncSession"]]
    ) -> None:
        self._session_factory = session_factory
        self._specialist = Specialist

    async def get_all(self, *, for_main: bool) -> list["SpecialistSchema"]:
        """Получить всех активных специалистов."""
        query = (
            select(self._specialist)
            .options(
                joinedload(self._specialist.specializations),
                joinedload(self._specialist.certificates),
            )
            .where(self._specialist.is_active.is_(True))
            .order_by(self._specialist.id)
        )

        if for_main:
            query = query.where(self._specialist.on_main.is_(True))

        async with self._session_factory() as session:
            rows = await session.execute(query)
            return [SpecialistSchema.from_orm(row) for row in rows.unique().scalars()]

    async def get(self, id: int) -> "SpecialistSchema":
        """Получить специалиста."""
        query = (
            select(self._specialist)
            .options(
                joinedload(self._specialist.specializations),
                joinedload(self._specialist.certificates),
            )
            .where(self._specialist.id == id, self._specialist.is_active.is_(True))
        )

        async with self._session_factory() as session:
            row = await session.execute(query)

            try:
                specialist = SpecialistSchema.from_orm(row.unique().one()[0])
            except NoResultFound as exc:
                message = f"Специалист с {id=} не найден."
                raise NotFoundError(message) from exc

        return specialist

    async def create_or_update(self, data: list["SourceSpecialistSchema"]) -> None:
        """Создание или обновление данных."""

        async with self._session_factory() as session:
            session.execute(insert(self._specialist), [specialist.dict() for specialist in data])


class SpecializationAdapter:
    """Адаптер для доступа к специальностям."""

    def __init__(
        self, session_factory: Callable[[], AbstractAsyncContextManager["AsyncSession"]]
    ) -> None:
        self._session_factory = session_factory
        self._specialization = Specialization

    async def get_all(self) -> list["SpecializationSchema"]:
        """Получить все специальности."""
        query = select(self._specialization)

        async with self._session_factory() as session:
            rows = await session.execute(query)
            return [SpecializationSchema.from_orm(row) for row in rows.unique().scalars()]
