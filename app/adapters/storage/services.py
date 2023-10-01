from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload

from app.adapters.storage.models import Service
from app.adapters.storage.pagination.query import get_query_with_meta
from app.adapters.storage.pagination.schemas import Paginated
from app.services.exceptions import NotFoundError
from app.services.schemas.services import ServiceSchema, ServiceTypeSchema, ServiceWithTypeSchema


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class ServicesAdapter:
    """Адаптер для доступа к данным услуг."""

    _session_factory: Callable[[], AbstractAsyncContextManager["AsyncSession"]]

    _service: ClassVar = Service

    async def get(self, id: str) -> "ServiceWithTypeSchema":
        """Получить услугу."""
        query = (
            select(self._service)
            .options(joinedload(self._service.service_type))
            .where(self._service.id == id, self._service.is_active.is_(True))
        )

        async with self._session_factory() as session:
            row = await session.execute(query)

            try:
                service = ServiceWithTypeSchema.model_validate(row.one()[0])
            except NoResultFound as exc:
                message = f"Услуга с {id=} не найден."
                raise NotFoundError(message) from exc

        return service

    async def get_all(self) -> list["ServiceTypeSchema"]:
        """Получить все категории услуг."""
        query = select(self._service_type).where(self._service_type.is_active.is_(True))

        async with self._session_factory() as session:
            rows = await session.execute(query)
            return [ServiceTypeSchema.model_validate(row) for row in rows.unique().scalars()]

    async def get_paginated(self, id: str, page: int, page_size: int) -> Paginated[ServiceSchema]:
        """Получить услуги по категории."""
        query = select(self._service).where(self._service.service_type_id == id, self._service.is_active.is_(True))

        async with self._session_factory() as session:
            paginated_query, paging = await get_query_with_meta(session, query, page, page_size)

            rows = await session.execute(paginated_query)
            services = [ServiceSchema.model_validate(row) for row in rows.unique().scalars()]

            if not services:
                message = f"Категория услуги с {id=} не найдена."
                raise NotFoundError(message)

        return Paginated[ServiceSchema](data=services, paging=paging)
