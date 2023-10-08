from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass
from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.sql.expression import func

from app.adapters.storage.models import Service, Category, Catalog, SpecialistService
from app.adapters.storage.pagination.query import get_query_with_meta
from app.adapters.storage.pagination.schemas import Paginated
from app.services.exceptions import NotFoundError
from app.services.schemas.services import ServiceSchema, CategorySchema, ServiceExtendedSchema
from app.services.updater.types import CatalogType


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class ServicesAdapter:
    """Адаптер для доступа к данным услуг."""

    _session_factory: Callable[[], AbstractAsyncContextManager["AsyncSession"]]

    async def get_categories(self, catalog_type: CatalogType) -> list["CategorySchema"]:
        """Получить категории услуг."""
        query = (
            select(Category.id, Category.name)
            .join(Catalog)
            .where(Catalog.page == catalog_type.value, Category.parent_id.is_(None))
        )

        async with self._session_factory() as session:
            rows = await session.execute(query)
            categories = [CategorySchema.model_validate(row) for row in rows.all()]

        return categories

    async def get(self, item_id: int, category_id: int, catalog_type: CatalogType) -> "ServiceExtendedSchema":
        """Получить услугу."""
        max_subquery = (
            select(func.max(SpecialistService.price))
            .where(SpecialistService.service_id == Service.id)
            .as_scalar()
            .label("price")
        )

        query = (
            select(
                Service.id,
                Service.name,
                Service.short_description,
                Service.description,
                Service.preparation,
                max_subquery,
                Category.id.label("category_id"),
                Category.name.label("category_name"),
            )
            .select_from(Service)
            .join(Service.categories)
            .join(Catalog)
            .where(Service.id == item_id, Category.id == category_id, Catalog.page == catalog_type.value)
        )

        async with self._session_factory() as session:
            row = await session.execute(query)

            try:
                service = ServiceExtendedSchema.model_validate(row.one())
            except NoResultFound as exc:
                message = f"Услуга с {service_id=} не найден."
                raise NotFoundError(message) from exc

        return service

    async def get_paginated(
        self, category_id: int, catalog_type: CatalogType, page: int, page_size: int
    ) -> Paginated[ServiceSchema]:
        """Получить услуги по категории."""
        max_subquery = (
            select(func.max(SpecialistService.price))
            .where(SpecialistService.service_id == Service.id)
            .as_scalar()
            .label("price")
        )

        query = (
            select(
                Service.id,
                Service.name,
                Service.short_description,
                max_subquery,
                Category.id.label("category_id"),
                Category.name.label("category_name"),
            )
            .select_from(Service)
            .join(Service.categories)
            .join(Catalog)
            .where(Category.id == category_id, Catalog.page == catalog_type.value)
        )

        async with self._session_factory() as session:
            paginated_query, paging = await get_query_with_meta(session, query, page, page_size)

            rows = await session.execute(paginated_query)
            services = [ServiceSchema.model_validate(row) for row in rows.all()]

            if not services:
                message = f"Категория услуги с {category_id=} не найдена."
                raise NotFoundError(message)

        return Paginated[ServiceSchema](data=services, paging=paging)
