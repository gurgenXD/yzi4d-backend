from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload, contains_eager
from sqlalchemy.sql.expression import func

from app.adapters.storage.models import Service, Category, Catalog, categories_services_table, SpecialistService
from app.adapters.storage.pagination.query import get_query_with_meta
from app.adapters.storage.pagination.schemas import Paginated
from app.services.exceptions import NotFoundError
from app.services.schemas.services import ServiceSchema, CategorySchema, ServiceWithTypeSchema
from app.services.updater.types import CatalogPageType


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class ServicesAdapter:
    """Адаптер для доступа к данным услуг."""

    _session_factory: Callable[[], AbstractAsyncContextManager["AsyncSession"]]

    _service: ClassVar = Service
    _category: ClassVar = Category
    _catalog: ClassVar = Catalog
    _specialist_service: ClassVar = SpecialistService
    _categories_services_table: ClassVar = categories_services_table

    async def get_categories(self, catalog_page: CatalogPageType) -> list["CategorySchema"]:
        """Получить категории услуг."""
        query = (
            select(self._category.id, self._category.name)
            .join(self._catalog)
            .where(
                self._catalog.page == catalog_page.value,
                self._category.is_active.is_(True),
                self._catalog.is_active.is_(True),
                self._category.parent_id.is_(None),
            )
        )

        async with self._session_factory() as session:
            rows = await session.execute(query)
            categories = [CategorySchema.model_validate(row) for row in rows.all()]

        return categories

    # async def get(self, id: str) -> "ServiceWithTypeSchema":
    #     """Получить услугу."""
    #     query = (
    #         select(self._service)
    #         .options(joinedload(self._service.service_type))
    #         .where(self._service.id == id, self._service.is_active.is_(True))
    #     )
    #
    #     async with self._session_factory() as session:
    #         row = await session.execute(query)
    #
    #         try:
    #             service = ServiceWithTypeSchema.model_validate(row.one()[0])
    #         except NoResultFound as exc:
    #             message = f"Услуга с {id=} не найден."
    #             raise NotFoundError(message) from exc
    #
    #     return service

    async def get_paginated(self, category_id: int, page: int, page_size: int) -> Paginated[ServiceSchema]:
        """Получить услуги по категории."""
        max_subquery = (
            select(func.max(self._specialist_service.price))
            .where(
                self._specialist_service.service_id == self._service.id, self._specialist_service.is_active.is_(True)
            )
            .as_scalar()
            .label("price")
        )

        query = (
            select(self._service.id, self._service.name, self._service.short_description, max_subquery)
            .join(self._service.categories)
            .where(
                self._category.id == category_id, self._service.is_active.is_(True), self._category.is_active.is_(True)
            )
        )

        async with self._session_factory() as session:
            paginated_query, paging = await get_query_with_meta(session, query, page, page_size)

            rows = await session.execute(paginated_query)
            services = [ServiceSchema.model_validate(row) for row in rows.all()]

            if not services:
                message = f"Категория услуги с {category_id=} не найдена."
                raise NotFoundError(message)

        return Paginated[ServiceSchema](data=services, paging=paging)
