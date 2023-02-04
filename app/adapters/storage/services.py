from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from app.adapters.storage.models import Service
from app.services.exceptions import NotFoundError
from app.services.schemas.services import ServiceSchema

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class ServicesAdapter:
    """Адаптер для доступа к данным услуг."""

    def __init__(
        self, session_factory: Callable[[], AbstractAsyncContextManager["AsyncSession"]]
    ) -> None:
        self._session_factory = session_factory
        self._service = Service

    async def get_all(self, on_main: bool) -> list["ServiceSchema"]:
        """Получить все активные услуги."""

        query = select(self._service).where(self._service.is_active.is_(True))

        if on_main:
            query = query.where(self._service.on_main.is_(True))

        async with self._session_factory() as session:
            rows = await session.execute(query)
            services = [ServiceSchema.from_orm(row) for row in rows.scalars()]

        return services

    async def get(self, id: int) -> "ServiceSchema":
        """Получить услугу."""

        query = select(self._service).where(
            self._service.id == id, self._service.is_active.is_(True)
        )

        async with self._session_factory() as session:
            row = await session.execute(query)

            try:
                service = ServiceSchema.from_orm(row.one()[0])
            except NoResultFound:
                raise NotFoundError(f"Услуга с {id=} не найден.")

        return service
