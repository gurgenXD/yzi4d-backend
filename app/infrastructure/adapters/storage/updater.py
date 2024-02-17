import base64
from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass
from datetime import UTC, datetime
from io import BytesIO
from itertools import groupby
from typing import TYPE_CHECKING

from fastapi import UploadFile
from PIL import Image
from sqlalchemy import delete, insert, select, update
from sqlalchemy.dialects.postgresql import insert as pg_insert

from app.domain.services.updater.types import UpdaterDataType, UpdaterStatusType
from app.infrastructure.adapters.storage.models import (
    Catalog,
    Category,
    Service,
    Specialist,
    SpecialistService,
    Specialization,
    Update,
    categories_services_table,
    specializations_specialists_table,
)


if TYPE_CHECKING:
    from logging import Logger

    from sqlalchemy.ext.asyncio import AsyncSession

    from app.domain.services.updater.schemas.services import CatalogItemSchema, CatalogSchema, ServiceExtSchema
    from app.domain.services.updater.schemas.specialists import SourceSpecialistSchema, SpecialistImageSchema


IMAGE_WIDTH = 525
CATALOG_MAP = {
    "16d8d12d-cee7-11ed-9ef0-3085a9a9a68d": "analyzes",
    "8d0be9eb-cedf-11ed-9ef0-3085a9a9a68d": "main",
    "bf1bb5b0-ea88-11ed-aeb5-bcee7b98e67c": "services",
}


@dataclass
class UpdaterAdapter:
    """Адаптер для доступа к данным обновления."""

    _session_factory: Callable[[], AbstractAsyncContextManager["AsyncSession"]]
    _logger: "Logger"

    async def start(self, data_type: UpdaterDataType) -> int:
        """Создать запись о начале обновления."""
        query = (
            insert(Update)
            .values(
                start_update=datetime.now(tz=UTC), status=UpdaterStatusType.PROCESSING.value, data_type=data_type.value,
            )
            .returning(Update.id)
        )

        async with self._session_factory() as session:
            row = await session.execute(query)
            return row.one()[0]

    async def finish(self, id_: int, status: UpdaterStatusType, message: str | None) -> None:
        """Обновить запись о завершении обновления."""
        query = (
            update(Update)
            .where(Update.id == id_)
            .values(end_update=datetime.now(tz=UTC), status=status.value, error_log=message)
        )

        async with self._session_factory() as session:
            await session.execute(query)

    async def save_catalogs(self, data: list["CatalogSchema"]) -> None:
        """Создание или обновление каталогов."""
        async with self._session_factory() as session:
            await session.execute(update(Catalog).values(is_active=False))

            for catalog in data:
                await session.execute(
                    pg_insert(Catalog)
                    .values(**catalog.model_dump(), page=CATALOG_MAP.get(catalog.guid))
                    .on_conflict_do_update(
                        index_elements=(Catalog.guid,),
                        set_={**catalog.model_dump(exclude={"guid"}), "page": CATALOG_MAP.get(catalog.guid)},
                    ),
                )

    async def save_categories(self, catalog_guid: str, data: list["CatalogItemSchema"]) -> None:
        """Создание или обновление категорий и связей с услугами."""
        async with self._session_factory() as session:
            catalog_id = (await session.execute(select(Catalog.id).where(Catalog.guid == catalog_guid))).scalar_one()

            await session.execute(update(Category).values(is_active=False).where(Category.catalog_id == catalog_id))

            for category in data:
                parent_id = (
                    await session.execute(select(Category.id).where(Category.guid == category.parent_guid))
                ).scalar()

                category_id = (
                    await session.execute(
                        pg_insert(Category)
                        .values(
                            catalog_id=catalog_id,
                            parent_id=parent_id,
                            **category.model_dump(exclude={"services", "parent_guid"}),
                        )
                        .on_conflict_do_update(
                            index_elements=(Category.guid,),
                            set_={
                                **category.model_dump(exclude={"services", "guid", "parent_guid"}),
                                "catalog_id": catalog_id,
                                "parent_id": parent_id,
                            },
                        ),
                    )
                ).inserted_primary_key[0]

                await session.execute(
                    delete(categories_services_table).where(
                        categories_services_table.c["service_category_id"] == category_id,
                    ),
                )

                for service in category.services:
                    if service_id := (
                        await session.execute(select(Service.id).where(Service.guid == service.guid))
                    ).scalar_one_or_none():
                        await session.execute(
                            insert(categories_services_table).values(
                                service_category_id=category_id, service_id=service_id,
                            ),
                        )
                    else:
                        self._logger.warning(f"Service '{service.guid}' doesn't exists. Category: {category_id}")

                await session.flush()

    async def save_services_with_prices(self, data: list["ServiceExtSchema"]) -> None:
        """Создание или обновление услуг и цен."""
        async with self._session_factory() as session:
            await session.execute(update(Service).values(is_active=False))
            await session.execute(update(SpecialistService).values(is_active=False))

            for service in data:
                service_id = (
                    await session.execute(
                        pg_insert(Service)
                        .values(service.model_dump(exclude={"prices", "is_hidden"}))
                        .on_conflict_do_update(
                            index_elements=(Service.guid,),
                            set_=service.model_dump(exclude={"prices", "guid", "is_hidden"}),
                        ),
                    )
                ).inserted_primary_key[0]

                groups = groupby(
                    sorted(service.prices, key=lambda x: x.specialist_guid), key=lambda x: x.specialist_guid,
                )

                for _, group_items in groups:
                    specialist_service = max(group_items, key=lambda x: x.price)

                    specialist_id = (
                        await session.execute(
                            select(Specialist.id).where(Specialist.guid == specialist_service.specialist_guid),
                        )
                    ).scalar_one()

                    await session.execute(
                        pg_insert(SpecialistService)
                        .values(
                            service_id=service_id,
                            specialist_id=specialist_id,
                            **specialist_service.model_dump(exclude={"office_guid", "specialist_guid"}),
                        )
                        .on_conflict_do_update(
                            index_elements=(SpecialistService.service_id, SpecialistService.specialist_id),
                            set_=specialist_service.model_dump(exclude={"office_guid", "specialist_guid"}),
                        ),
                    )

                await session.flush()

    async def save_specialists(self, data: list["SourceSpecialistSchema"]) -> None:
        """Создание или обновление специалистов и специальностей."""
        async with self._session_factory() as session:
            await session.execute(update(Specialist).values(is_active=False))
            await session.execute(update(Specialization).values(is_active=False))

            await session.execute(delete(specializations_specialists_table))

            for specialist in data:
                specialist_id = (
                    await session.execute(
                        pg_insert(Specialist)
                        .values(specialist.model_dump(exclude={"specializations", "is_hidden"}))
                        .on_conflict_do_update(
                            index_elements=(Specialist.guid,),
                            set_=specialist.model_dump(exclude={"specializations", "guid", "is_hidden"}),
                        ),
                    )
                ).inserted_primary_key[0]

                for specialization in specialist.specializations:
                    specialization_id = (
                        await session.execute(
                            pg_insert(Specialization)
                            .values(specialization.model_dump(exclude={"is_hidden"}))
                            .on_conflict_do_update(
                                index_elements=(Specialization.guid,),
                                set_=specialization.model_dump(exclude={"guid", "is_hidden"}),
                            ),
                        )
                    ).inserted_primary_key[0]

                    await session.execute(
                        insert(specializations_specialists_table).values(
                            specialization_id=specialization_id, specialist_id=specialist_id,
                        ),
                    )

                await session.flush()

    async def get_specialists_guids(self) -> list[str]:
        """Получить guid специалистов."""
        async with self._session_factory() as session:
            guids = (
                (await session.execute(select(Specialist.guid).where(Specialist.is_active.is_(True)))).scalars().all()
            )
            return list(guids)

    async def save_image(self, guid: str, image: "SpecialistImageSchema") -> None:
        """Сохранить фотографию."""
        file = (
            UploadFile(self._resize_image(BytesIO(base64.b64decode(image.data))), filename=f"{guid}.jpg")
            if image.data
            else None
        )

        async with self._session_factory() as session:
            await session.execute(update(Specialist).where(Specialist.guid == guid).values(photo=file))

    @staticmethod
    def _resize_image(data: "BytesIO") -> "BytesIO":
        """Изменить размер картинки."""
        img = Image.open(data)
        img = img.convert("RGB")
        hsize = int(float(img.size[1]) * float(IMAGE_WIDTH / float(img.size[0])))

        img = img.resize((IMAGE_WIDTH, hsize), Image.Resampling.LANCZOS)

        output = BytesIO()
        img.save(output, format="JPEG")

        return BytesIO(output.getvalue())
