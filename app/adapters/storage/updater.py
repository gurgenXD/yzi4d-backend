from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import TYPE_CHECKING, ClassVar
from itertools import groupby
from sqlalchemy.dialects.postgresql import insert as pg_insert
import base64
from io import BytesIO
from fastapi import UploadFile

from sqlalchemy import update, select, delete, insert

from app.adapters.storage.models import (
    Service,
    Catalog,
    Category,
    SpecialistService,
    categories_services_table,
    Specialist,
    Update,
    Specialization,
    specializations_specialists_table,
)
from app.services.updater.types import UpdaterStatusType, UpdaterDataType


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from app.services.updater.schemas.services import CatalogSchema, CatalogItemSchema, ServiceExtSchema
    from app.services.updater.schemas.specialists import SourceSpecialistSchema, SpecialistImageSchema


@dataclass
class UpdaterAdapter:
    """Адаптер для доступа к данным обновления."""

    _session_factory: Callable[[], AbstractAsyncContextManager["AsyncSession"]]

    _updater: ClassVar = Update
    _service: ClassVar = Service
    _catalog: ClassVar = Catalog
    _category: ClassVar = Category
    _specialist_service: ClassVar = SpecialistService
    _specialist: ClassVar = Specialist
    _specialization: ClassVar = Specialization
    _categories_services_table: ClassVar = categories_services_table
    _specializations_specialists_table: ClassVar = specializations_specialists_table

    async def start(self, data_type: UpdaterDataType) -> int:
        """Создать запись о начале обновления."""
        query = (
            insert(self._updater)
            .values(
                start_update=datetime.now(tz=timezone.utc),
                status=UpdaterStatusType.PROCESSING.value,
                data_type=data_type.value,
            )
            .returning(self._updater.id)
        )

        async with self._session_factory() as session:
            row = await session.execute(query)
            return row.one()[0]

    async def finish(self, id: int, status: UpdaterStatusType, message: str | None) -> None:
        """Обновить запись о завершении обновления."""
        query = (
            update(self._updater)
            .where(self._updater.id == id)
            .values(end_update=datetime.now(tz=timezone.utc), status=status.value, error_log=message)
        )

        async with self._session_factory() as session:
            await session.execute(query)

    async def save_catalogs(self, data: list["CatalogSchema"]) -> None:
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

    async def save_categories(self, catalog_guid: str, data: list["CatalogItemSchema"]) -> None:
        """Создание или обновление категорий и связей с услугами."""
        async with self._session_factory() as session:
            catalog_id = (
                await session.execute(select(self._catalog.id).where(self._catalog.guid == catalog_guid))
            ).scalar_one()

            await session.execute(
                update(self._category).values(is_active=False).where(self._category.catalog_id == catalog_id)
            )
            await session.execute(delete(self._categories_services_table))

            for category in data:
                parent_id = (
                    await session.execute(select(self._category.id).where(self._category.guid == category.parent_guid))
                ).scalar()

                category_id = (
                    await session.execute(
                        pg_insert(self._category)
                        .values(
                            catalog_id=catalog_id,
                            parent_id=parent_id,
                            **category.model_dump(exclude={"services", "parent_guid"}),
                        )
                        .on_conflict_do_update(
                            index_elements=(self._category.guid,),
                            set_={
                                **category.model_dump(exclude={"services", "guid", "parent_guid"}),
                                "catalog_id": catalog_id,
                                "parent_id": parent_id,
                            },
                        )
                    )
                ).inserted_primary_key[0]

                for service in category.services:
                    service_id = (
                        await session.execute(select(self._service.id).where(self._service.guid == service.guid))
                    ).scalar_one()

                    await session.execute(
                        pg_insert(self._categories_services_table)
                        .values(service_category_id=category_id, service_id=service_id)
                        .on_conflict_do_nothing(
                            index_elements=(
                                self._categories_services_table.c["service_category_id"],
                                self._categories_services_table.c["service_id"],
                            )
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
                        .values(service.model_dump(exclude={"prices", "is_hidden"}))
                        .on_conflict_do_update(
                            index_elements=(self._service.guid,),
                            set_=service.model_dump(exclude={"prices", "guid", "is_hidden"}),
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

    async def save_specialists(self, data: list["SourceSpecialistSchema"]) -> None:
        """Создание или обновление специалистов и специальностей."""
        async with self._session_factory() as session:
            await session.execute(update(self._specialist).values(is_active=False))
            await session.execute(update(self._specialization).values(is_active=False))

            await session.execute(delete(self._specializations_specialists_table))

            for specialist in data:
                specialist_id = (
                    await session.execute(
                        pg_insert(self._specialist)
                        .values(specialist.model_dump(exclude={"specializations", "is_hidden"}))
                        .on_conflict_do_update(
                            index_elements=(self._specialist.guid,),
                            set_=specialist.model_dump(exclude={"specializations", "guid", "is_hidden"}),
                        )
                    )
                ).inserted_primary_key[0]

                for specialization in specialist.specializations:
                    specialization_id = (
                        await session.execute(
                            pg_insert(self._specialization)
                            .values(specialization.model_dump())
                            .on_conflict_do_update(
                                index_elements=(self._specialization.guid,),
                                set_=specialization.model_dump(exclude={"guid"}),
                            )
                        )
                    ).inserted_primary_key[0]

                    await session.execute(
                        pg_insert(self._specializations_specialists_table)
                        .values(specialization_id=specialization_id, specialist_id=specialist_id)
                        .on_conflict_do_nothing(
                            index_elements=(
                                self._specializations_specialists_table.c["specialization_id"],
                                self._specializations_specialists_table.c["specialist_id"],
                            )
                        )
                    )

                await session.flush()

    async def get_specialists_guids(self) -> list[str]:
        """Получить guid специалистов."""
        async with self._session_factory() as session:
            guids = (
                (await session.execute(select(self._specialist.guid).where(self._specialist.is_active.is_(True))))
                .scalars()
                .all()
            )
            return list(guids)

    async def save_image(self, guid: str, image: "SpecialistImageSchema") -> None:
        """Сохранить фотографию."""
        async with self._session_factory() as session:
            file = UploadFile(BytesIO(base64.b64decode(image.data)), filename=f"{guid}.jpg")
            await session.execute(update(self._specialist).where(self._specialist.guid == guid).values(photo=file))
