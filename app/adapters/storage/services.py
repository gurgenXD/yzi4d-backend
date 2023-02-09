from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload

from app.adapters.storage.models import Service, ServiceType
from app.services.exceptions import NotFoundError
from app.services.schemas.services import (
    ServiceSchema,
    ServiceTypeSchema,
    ServiceTypeWithServicesSchema,
)

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class ServicesAdapter:
    """Адаптер для доступа к данным услуг."""

    def __init__(
        self, session_factory: Callable[[], AbstractAsyncContextManager["AsyncSession"]]
    ) -> None:
        self._session_factory = session_factory
        self._service = Service

    async def get_all(self, for_main: bool) -> list["ServiceSchema"]:
        """Получить все активные услуги."""

        query = select(self._service).where(self._service.is_active.is_(True))

        if for_main:
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


class ServiceTypeAdapter:
    """Адаптер для доступа к категориям услуг."""

    def __init__(
        self, session_factory: Callable[[], AbstractAsyncContextManager["AsyncSession"]]
    ) -> None:
        self._session_factory = session_factory
        self._service_type = ServiceType

    async def get_all(self) -> list["ServiceTypeSchema"]:
        """Получить все категории услуг."""

        query = select(self._service_type).where(self._service_type.is_active.is_(True))

        async with self._session_factory() as session:
            rows = await session.execute(query)
            service_types = [ServiceTypeSchema.from_orm(row) for row in rows.unique().scalars()]

        return service_types

    async def get(self, id: int) -> "ServiceTypeWithServicesSchema":
        """Получить категорию услуги."""

        query = (
            select(self._service_type)
            .options(joinedload(self._service_type.services))
            .where(self._service_type.id == id, self._service_type.is_active.is_(True))
        )

        async with self._session_factory() as session:
            row = await session.execute(query)

            try:
                service_type = ServiceTypeWithServicesSchema.from_orm(row.unique().one()[0])
            except NoResultFound:
                raise NotFoundError(f"Категория услуги с {id=} не найдена.")

        return service_type
