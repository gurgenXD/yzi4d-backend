from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

from sqlalchemy import update, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload
from itertools import groupby

from app.adapters.storage.models import Service, Catalog, Category, SpecialistService
from app.adapters.storage.pagination.query import get_query_with_meta
from app.adapters.storage.pagination.schemas import Paginated
from app.services.exceptions import NotFoundError
from app.services.schemas.services import ServiceSchema, ServiceTypeSchema, ServiceWithTypeSchema


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from app.services.updater.schemas.services import (
        CatalogSchema,
        CatalogItemSchema,
        ServiceExtSchema,
    )


@dataclass
class ServicesAdapter:
    """Адаптер для доступа к данным услуг."""

    _session_factory: Callable[[], AbstractAsyncContextManager["AsyncSession"]]

    _service: ClassVar = Service
    _catalog: ClassVar = Catalog
    _category: ClassVar = Category
    _specialist_service: ClassVar = SpecialistService

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

    async def create_or_update_catalogs(self, data: list["CatalogSchema"]) -> None:
        """Создание или обновление каталогов."""
        async with self._session_factory() as session:
            await session.execute(update(self._catalog).values(is_active=False))

            for catalog in data:
                catalog = self._catalog(**catalog.model_dump())
                await session.merge(catalog)

    async def create_or_update_categories(self, data: list["CatalogItemSchema"]) -> None:
        """Создание или обновление категорий и связей с услугами."""
        async with self._session_factory() as session:
            await session.execute(update(self._category).values(is_active=False))

            for category in data:
                category_model = self._category(**category.model_dump(exclude={"services"}))

                services: list["Service"] = []
                for service in category.services:
                    service_model = self._service(**service.model_dump())
                    services.append(service_model)

                category_model.services[:] = services
                await session.merge(service_model)
                await session.flush()
                session.expunge_all()

    async def create_or_update(self, data: list["ServiceExtSchema"]) -> None:
        """Создание или обновление услуг и цен."""
        async with self._session_factory() as session:
            await session.execute(update(self._service).values(is_active=False))
            await session.execute(update(self._specialist_service).values(is_active=False))

            for service in data:
                service_model = self._service(**service.model_dump(exclude={"prices"}))
                await session.merge(service_model)

                groups = groupby(
                    sorted(service.prices, key=lambda x: x.specialist_id),
                    key=lambda x: x.specialist_id,
                )

                for _, group_items in groups:
                    specialist_service = max(group_items, key=lambda x: x.price)

                    specialist_service_model = self._specialist_service(
                        service_id=service_model.id,
                        specialist_id=specialist_service.specialist_id,
                        **specialist_service.model_dump(exclude={"office_id", "specialist_id"}),
                    )
                    await session.merge(specialist_service_model)

                await session.flush()
                session.expunge_all()


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
            return [ServiceTypeSchema.model_validate(row) for row in rows.unique().scalars()]

    async def get_paginated(self, id: str, page: int, page_size: int) -> Paginated[ServiceSchema]:
        """Получить услуги по категории."""
        query = select(self._service).where(
            self._service.service_type_id == id, self._service.is_active.is_(True)
        )

        async with self._session_factory() as session:
            paginated_query, paging = await get_query_with_meta(session, query, page, page_size)

            rows = await session.execute(paginated_query)
            services = [ServiceSchema.model_validate(row) for row in rows.unique().scalars()]

            if not services:
                message = f"Категория услуги с {id=} не найдена."
                raise NotFoundError(message)

        return Paginated[ServiceSchema](data=services, paging=paging)
