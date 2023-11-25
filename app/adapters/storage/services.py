from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass
from typing import TYPE_CHECKING
from itertools import groupby

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.sql.expression import func

from app.adapters.storage.models import Service, Category, Catalog, SpecialistService, categories_services_table
from app.adapters.storage.pagination.query import get_query_with_meta
from app.adapters.storage.pagination.schemas import Paginated
from app.services.exceptions import NotFoundError
from app.services.schemas.services import ServiceSchema, CategorySchema, StrictServiceSchema
from app.services.updater.types import CatalogType


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy import Select


@dataclass
class ServicesAdapter:
    """Адаптер для доступа к данным услуг."""

    _session_factory: Callable[[], AbstractAsyncContextManager["AsyncSession"]]

    async def get_categories(
        self, catalog_type: CatalogType, category_id: int | None, search_query: str | None
    ) -> list[CategorySchema]:
        """Получить категории."""
        query = self._service_query(catalog_type).with_only_columns(Category.id, Category.name).order_by(Category.name)

        if category_id:
            query = query.where(Category.id == category_id)

        if search_query:
            search_query = search_query.strip()
            query = query.where(Service.name.ilike(f"%{search_query}%"))

        async with self._session_factory() as session:
            rows = (await session.execute(query)).unique().all()
            return [CategorySchema.model_validate(row) for row in rows]

    async def get_categories_with_services(self, catalog_type: CatalogType) -> list["CategorySchema"]:
        """Получить категории услуг с услугами."""
        query = self._service_query(catalog_type).order_by(Category.name)

        async with self._session_factory() as session:
            rows = (await session.execute(query)).unique().all()

            categories = [
                CategorySchema(
                    id=key[0],
                    name=key[1],
                    services=[StrictServiceSchema.model_validate(service) for service in services],
                )
                for key, services in groupby(rows, lambda row: (row.category_id, row.category_name))
            ]

        return categories

    async def get(self, item_id: int, category_id: int, catalog_type: CatalogType) -> "ServiceSchema":
        """Получить услугу."""
        query = self._service_query(catalog_type, category_id).where(Service.id == item_id)

        async with self._session_factory() as session:
            row = await session.execute(query)

            try:
                service = ServiceSchema.model_validate(row.one())
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
        self, catalog_type: CatalogType, category_id: int | None, search_query: str | None, page: int, page_size: int
    ) -> Paginated[ServiceSchema]:
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
            services = [ServiceSchema.model_validate(row) for row in rows.all()]

        return Paginated[ServiceSchema](data=services, paging=paging)

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
