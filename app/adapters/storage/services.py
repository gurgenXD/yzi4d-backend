from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

from sqlalchemy import update, select, delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload
from itertools import groupby
from sqlalchemy.dialects.postgresql import insert as pg_insert

from app.adapters.storage.models import (
    Service,
    Catalog,
    Category,
    SpecialistService,
    categories_services_table,
    Specialist,
)
from app.adapters.storage.pagination.query import get_query_with_meta
from app.adapters.storage.pagination.schemas import Paginated
from app.services.exceptions import NotFoundError
from app.services.schemas.services import ServiceSchema, ServiceTypeSchema, ServiceWithTypeSchema


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from app.services.updater.schemas.services import CatalogSchema, CatalogItemSchema, ServiceExtSchema


@dataclass
class ServicesAdapter:
    """Адаптер для доступа к данным услуг."""

    _session_factory: Callable[[], AbstractAsyncContextManager["AsyncSession"]]

    _service: ClassVar = Service
    _catalog: ClassVar = Catalog
    _category: ClassVar = Category
    _specialist_service: ClassVar = SpecialistService
    _specialist: ClassVar = Specialist
    _relations: ClassVar = categories_services_table

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

    async def create_or_update_catalogs(self, data: list["CatalogSchema"]) -> None:
        """Создание или обновление каталогов."""
        async with self._session_factory() as session:
            await session.execute(update(self._catalog).values(is_active=False))

            for catalog in data:
                await session.execute(
                    pg_insert(self._catalog)
                    .values(catalog.model_dump())
                    .on_conflict_do_update(
                        index_elements=(self._catalog.guid,), set_=catalog.model_dump(exclude={"guid"})
                    )
                )

    async def create_or_update_categories(self, catalog_guid: str, data: list["CatalogItemSchema"]) -> None:
        """Создание или обновление категорий и связей с услугами."""
        async with self._session_factory() as session:
            await session.execute(update(self._category).values(is_active=False))

            await session.execute(delete(self._relations))

            catalog_id = (
                await session.execute(select(self._catalog.id).where(self._catalog.guid == catalog_guid))
            ).scalar_one()

            for category in data:
                category_id = (
                    await session.execute(
                        pg_insert(self._category)
                        .values(catalog_id=catalog_id, **category.model_dump(exclude={"services"}))
                        .on_conflict_do_update(
                            index_elements=(self._category.guid,),
                            set_={**category.model_dump(exclude={"services", "guid"}), "catalog_id": catalog_id},
                        )
                    )
                ).inserted_primary_key[0]

                for service in category.services:
                    # FIXME: удалить костыль
                    if service.guid in {
                        "e38b47fb-f865-11ea-8a7e-107b441820e7",
                        "e38b47fc-f865-11ea-8a7e-107b441820e7",
                        "214b0cac-e183-11eb-bdf6-107b441820e7",
                        "11515b7e-e51c-11ed-aeb5-bcee7b98e67c",
                        "8b7fd040-5edc-11eb-a481-107b441820e7",
                        "7f0d471c-f1e6-11ea-b4f5-107b441820e7",
                    }:
                        continue

                    service_id = (
                        await session.execute(select(self._service.id).where(self._service.guid == service.guid))
                    ).scalar_one()

                    await session.execute(
                        pg_insert(self._relations)
                        .values(service_category_id=category_id, service_id=service_id)
                        .on_conflict_do_nothing(
                            index_elements=(self._relations.c["service_category_id"], self._relations.c["service_id"])
                        )
                    )

                await session.flush()

    async def save_services_with_prices(self, data: list["ServiceExtSchema"]) -> None:
        """Создание или обновление услуг и цен."""
        async with self._session_factory() as session:
            await session.execute(update(self._service).values(is_active=False))
            await session.execute(update(self._specialist_service).values(is_active=False))

            for service in data:
                service_id = (
                    await session.execute(
                        pg_insert(self._service)
                        .values(service.model_dump(exclude={"prices"}))
                        .on_conflict_do_update(
                            index_elements=(self._service.guid,), set_=service.model_dump(exclude={"prices", "guid"})
                        )
                    )
                ).inserted_primary_key[0]

                groups = groupby(
                    sorted(service.prices, key=lambda x: x.specialist_guid), key=lambda x: x.specialist_guid
                )

                for _, group_items in groups:
                    specialist_service = max(group_items, key=lambda x: x.price)

                    specialist_id = (
                        await session.execute(
                            select(self._specialist.id).where(
                                self._specialist.guid == specialist_service.specialist_guid
                            )
                        )
                    ).scalar_one()

                    await session.execute(
                        pg_insert(self._specialist_service)
                        .values(
                            service_id=service_id,
                            specialist_id=specialist_id,
                            **specialist_service.model_dump(exclude={"office_guid", "specialist_guid"}),
                        )
                        .on_conflict_do_update(
                            index_elements=(
                                self._specialist_service.service_id,
                                self._specialist_service.specialist_id,
                            ),
                            set_=specialist_service.model_dump(exclude={"office_guid", "specialist_guid"}),
                        )
                    )

                await session.flush()
