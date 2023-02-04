from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload

from app.adapters.storage.models import Specialist
from app.services.exceptions import NotFoundError
from app.services.schemas.specialists import SpecialistSchema

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class SpecialistsAdapter:
    """Адаптер для доступа к данным специалистов."""

    def __init__(
        self, session_factory: Callable[[], AbstractAsyncContextManager["AsyncSession"]]
    ) -> None:
        self._session_factory = session_factory
        self._specialist = Specialist

    async def get_all(self, on_main: bool) -> list["SpecialistSchema"]:
        """Получить всех активных специалистов."""

        query = (
            select(self._specialist)
            .options(joinedload(self._specialist.specializations))
            .where(self._specialist.is_active.is_(True))
            .order_by(self._specialist.id)
        )

        if on_main:
            query = query.where(self._specialist.on_main.is_(True))

        async with self._session_factory() as session:
            rows = await session.execute(query)
            specialists = [SpecialistSchema.from_orm(row) for row in rows.unique().scalars()]

        return specialists

    async def get(self, id: int) -> "SpecialistSchema":
        """Получить специалиста."""

        query = select(self._specialist).where(
            self._specialist.id == id, self._specialist.is_active.is_(True)
        )

        async with self._session_factory() as session:
            row = await session.execute(query)

            try:
                specialist = SpecialistSchema.from_orm(row.one()[0])
            except NoResultFound:
                raise NotFoundError(f"Специалист с {id=} не найден.")

        return specialist