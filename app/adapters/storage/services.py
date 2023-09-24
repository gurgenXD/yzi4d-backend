from collections import defaultdict
from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

from sqlalchemy import insert, select, text
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload

# from app.adapters.storage.models import Service
from app.adapters.storage.pagination.query import get_query_with_meta
from app.adapters.storage.pagination.schemas import Paginated
from app.services.exceptions import NotFoundError
from app.services.schemas.services import ServiceSchema, ServiceTypeSchema, ServiceWithTypeSchema
from utils.chunks import divide_chunks


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from app.services.updater.schemas.services import SourceServiceGroupSchema, SourceServiceSchema


CHUNK_SIZE = 100


@dataclass
class ServicesAdapter:
    """Адаптер для доступа к данным услуг."""

    _session_factory: Callable[[], AbstractAsyncContextManager["AsyncSession"]]

    # _service: ClassVar = Service

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
                service = ServiceWithTypeSchema.from_orm(row.one()[0])
            except NoResultFound as exc:
                message = f"Услуга с {id=} не найден."
                raise NotFoundError(message) from exc

        return service

    async def create_or_update_groups(self, data: list["SourceServiceGroupSchema"]) -> None:
        """Создание или обновление данных групп."""
        groups = defaultdict(list)
        for service_group in data:
            groups[service_group.level].append(service_group)

        async with self._session_factory() as session:
            await session.execute(text(f"TRUNCATE {self._service.__tablename__} CASCADE;"))

            for _, service_groups in sorted(groups.items(), key=lambda item: item[0]):
                await session.execute(
                    insert(self._service),
                    [service_group.dict() for service_group in service_groups],
                )
                await session.flush()

    async def create_or_update(self, data: list["SourceServiceSchema"]) -> None:
        """Создание или обновление данных."""
        async with self._session_factory() as session:
            for services in divide_chunks(data, CHUNK_SIZE):
                await session.execute(
                    insert(self._service), [service.dict() for service in services]
                )
                await session.flush()


@dataclass
class ServiceTypeAdapter:
    """Адаптер для доступа к категориям услуг."""

    _session_factory: Callable[[], AbstractAsyncContextManager["AsyncSession"]]

    # _service: ClassVar = Service

    async def get_all(self) -> list["ServiceTypeSchema"]:
        """Получить все категории услуг."""
        query = select(self._service_type).where(self._service_type.is_active.is_(True))

        async with self._session_factory() as session:
            rows = await session.execute(query)
            return [ServiceTypeSchema.from_orm(row) for row in rows.unique().scalars()]

    async def get_paginated(self, id: str, page: int, page_size: int) -> Paginated[ServiceSchema]:
        """Получить услуги по категории."""
        query = select(self._service).where(
            self._service.service_type_id == id, self._service.is_active.is_(True)
        )

        async with self._session_factory() as session:
            paginated_query, paging = await get_query_with_meta(session, query, page, page_size)

            rows = await session.execute(paginated_query)
            services = [ServiceSchema.from_orm(row) for row in rows.unique().scalars()]

            if not services:
                message = f"Категория услуги с {id=} не найдена."
                raise NotFoundError(message)

        return Paginated[ServiceSchema](data=services, paging=paging)
