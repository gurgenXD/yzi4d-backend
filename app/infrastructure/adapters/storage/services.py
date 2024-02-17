from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass
from itertools import groupby
from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.sql.expression import func

from app.domain.entities.services import CategoryEntity, ServiceEntity, StrictServiceEntity
from app.domain.services.exceptions import NotFoundError
from app.domain.services.updater.types import CatalogType
from app.infrastructure.adapters.storage.models import (
    Catalog,
    Category,
    Service,
    SpecialistService,
    categories_services_table,
)
from app.infrastructure.adapters.storage.pagination.query import get_query_with_meta
from app.infrastructure.adapters.storage.pagination.schemas import Paginated


if TYPE_CHECKING:
    from sqlalchemy import Select
    from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class ServicesAdapter:
    """Адаптер для доступа к данным услуг."""

    _session_factory: Callable[[], AbstractAsyncContextManager["AsyncSession"]]

    async def get_categories(
        self, catalog_type: CatalogType, category_id: int | None, search_query: str | None,
    ) -> list[CategoryEntity]:
        """Получить категории."""
        query = self._service_query(catalog_type).with_only_columns(Category.id, Category.name).order_by(Category.name)

        if category_id:
            query = query.where(Category.id == category_id)

        if search_query:
            search_query = search_query.strip()
            query = query.where(Service.name.ilike(f"%{search_query}%"))

        async with self._session_factory() as session:
            rows = (await session.execute(query)).unique().all()
            return [CategoryEntity.model_validate(row) for row in rows]

    async def get_categories_with_services(self, base_url: str, catalog_type: CatalogType) -> list["CategoryEntity"]:
        """Получить категории услуг с услугами."""
        query = self._service_query(catalog_type).order_by(Category.name)

        async with self._session_factory() as session:
            rows = (await session.execute(query)).unique().all()

            return [
                CategoryEntity(
                    id=key[0],
                    name=key[1],
                    icon=f"{base_url}media/categories/{key[2].name}" if key[2] else None,
                    services=[StrictServiceEntity.model_validate(service) for service in services],
                )
                for key, services in groupby(rows, lambda row: (row.category_id, row.category_name, row.icon))
            ]

    async def get(self, item_id: int, category_id: int, catalog_type: CatalogType) -> "ServiceEntity":
        """Получить услугу."""
        query = self._service_query(catalog_type, category_id).where(Service.id == item_id)

        async with self._session_factory() as session:
            row = await session.execute(query)

            try:
                service = ServiceEntity.model_validate(row.one())
            except NoResultFound as exc:
                message = f"Услуга с {item_id=} не найден."
                raise NotFoundError(message) from exc

        return service

    async def convert_category_id(self, service_id: int, catalog_type: CatalogType) -> int | None:
        """Получить услугу."""
        query = (
            select(categories_services_table.c["service_category_id"])
            .join(Category)
            .join(Catalog)
            .where(
                Catalog.page == catalog_type.value,
                categories_services_table.c["service_id"] == service_id,
                Category.is_active.is_(True),
                Catalog.is_active.is_(True),
            )
        )

        async with self._session_factory() as session:
            row = await session.execute(query)

            return row.scalar()

    async def get_paginated(
        self, catalog_type: CatalogType, category_id: int | None, search_query: str | None, page: int, page_size: int,
    ) -> Paginated[ServiceEntity]:
        """Получить услуги по категории."""
        async with self._session_factory() as session:
            if category_id == -1 and (categories := await self.get_categories(catalog_type, None, search_query)):
                category_id = categories[0].id

            query = self._service_query(catalog_type, category_id).order_by(Service.name)

            if search_query:
                search_query = search_query.strip()
                query = query.where(Service.name.ilike(f"%{search_query}%"))

            paginated_query, paging = await get_query_with_meta(session, query, page, page_size)

            rows = await session.execute(paginated_query)
            services = [ServiceEntity.model_validate(row) for row in rows.all()]

        return Paginated[ServiceEntity](data=services, paging=paging)

    @staticmethod
    def _service_query(catalog_type: CatalogType, category_id: int | None = None) -> "Select":
        """Запрос на получении услуги."""
        max_subquery = (
            select(func.max(SpecialistService.price))
            .where(SpecialistService.service_id == Service.id, SpecialistService.is_active.is_(True))
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
                Category.icon,
                Category.id.label("category_id"),
                Category.name.label("category_name"),
            )
            .select_from(Service)
            .join(Service.categories)
            .join(Catalog)
            .where(
                Catalog.page == catalog_type.value,
                Service.is_active.is_(True),
                Catalog.is_active.is_(True),
                Category.is_active.is_(True),
            )
        )

        if category_id:
            query = query.where(Category.id == category_id)

        return query
