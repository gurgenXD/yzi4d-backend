import random
from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass
from typing import TYPE_CHECKING

from sqlalchemy import or_, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import contains_eager

from app.domain.entities.services import ServiceEntity
from app.domain.entities.specialists import SpecialistEntity
from app.domain.services.exceptions import NotFoundError
from app.domain.services.updater.types import CatalogType
from app.infrastructure.adapters.storage.models import (
    Catalog,
    Category,
    Service,
    Specialist,
    SpecialistService,
    Specialization,
)
from app.infrastructure.adapters.storage.pagination.query import get_query_with_meta
from app.infrastructure.adapters.storage.pagination.schemas import Paginated


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class SpecialistsAdapter:
    """Адаптер для доступа к данным специалистов."""

    _session_factory: Callable[[], AbstractAsyncContextManager["AsyncSession"]]

    async def get_paginated(
        self,
        *,
        base_url: str,
        can_online: bool = False,
        can_adult: bool = False,
        can_child: bool = False,
        search_query: str | None = None,
        specialization_id: str | None = None,
        page: int = 1,
        page_size: int = 1,
    ) -> Paginated[SpecialistEntity]:
        """Получить всех активных специалистов."""
        query = select(Specialist.id).where(Specialist.is_active.is_(True)).order_by(Specialist.surname)

        if can_online:
            query = query.where(Specialist.can_online.is_(True))

        if can_adult:
            query = query.where(Specialist.can_adult.is_(True))

        if can_child:
            query = query.where(Specialist.can_child.is_(True))

        if search_query:
            search_query = search_query.strip()
            query = query.where(
                or_(Specialist.surname.ilike(f"%{search_query}%"), Specialist.name.ilike(f"%{search_query}%")),
            )

        if specialization_id:
            query = query.join(Specialist.specializations, isouter=True).where(
                Specialization.id == specialization_id, Specialization.is_active.is_(True),
            )

        async with self._session_factory() as session:
            paginated_query, paging = await get_query_with_meta(session, query, page, page_size)

            subquery = paginated_query.subquery()
            join_query = (
                select(Specialist)
                .join(subquery, Specialist.id == subquery.c.id)
                .join(Specialist.specializations, isouter=True)
                .join(Specialist.certificates, isouter=True)
                .options(contains_eager(Specialist.specializations), contains_eager(Specialist.certificates))
                .order_by(Specialist.surname)
            )

            rows = await session.execute(join_query)

            specialists: list["SpecialistEntity"] = []
            for row in rows.unique().scalars():
                specialist = SpecialistEntity.model_validate(row)
                specialist.photo = f"{base_url}media/specialists/{row.photo.name}" if row.photo else None
                specialists.append(specialist)

            return Paginated[SpecialistEntity](data=specialists, paging=paging)

    async def get_shuffled(self, *, base_url: str, limit: int) -> list["SpecialistEntity"]:
        """Получить всех активных специалистов."""
        query = (
            select(Specialist)
            .where(Specialist.is_active.is_(True), Specialist.on_main.is_(True), Specialist.photo.is_not(None))
            .join(Specialist.specializations, isouter=True)
            .options(contains_eager(Specialist.specializations))
        )

        async with self._session_factory() as session:
            rows = (await session.execute(query)).unique().scalars().all()
            rand_specialists = random.sample(rows, limit) if len(rows) > limit else rows

            specialists: list["SpecialistEntity"] = []
            for row in rand_specialists:
                specialist = SpecialistEntity(**row.__dict__)
                specialist.photo = f"{base_url}media/specialists/{row.photo.name}"
                specialists.append(specialist)

            return specialists

    async def get(self, base_url: str, item_id: int) -> "SpecialistEntity":
        """Получить специалиста."""
        query = (
            select(Specialist)
            .join(Specialist.specializations, isouter=True)
            .join(Specialist.certificates, isouter=True)
            .options(contains_eager(Specialist.specializations), contains_eager(Specialist.certificates))
            .where(Specialist.id == item_id, Specialist.is_active.is_(True), Specialization.is_active.is_(True))
        )

        async with self._session_factory() as session:
            row = await session.execute(query)

            try:
                row_data = row.unique().one()[0]
                specialist = SpecialistEntity.model_validate(row_data)
                specialist.photo = f"{base_url}media/specialists/{row_data.photo.name}" if row_data.photo else None
            except NoResultFound as exc:
                message = f"Специалист с {item_id=} не найден."
                raise NotFoundError(message) from exc

        return specialist

    async def get_services(
        self, item_id: int, catalog_page: CatalogType, page: int, page_size: int,
    ) -> Paginated[ServiceEntity]:
        """Получить услуги специалиста."""
        query = (
            select(
                Service.id,
                Service.name,
                Service.short_description,
                Service.preparation,
                Service.description,
                SpecialistService.price,
                Category.id.label("category_id"),
                Category.name.label("category_name"),
            )
            .select_from(Service)
            .join(SpecialistService)
            .join(Service.categories)
            .join(Catalog)
            .where(
                SpecialistService.specialist_id == item_id,
                Catalog.page == catalog_page.value,
                Service.is_active.is_(True),
                SpecialistService.is_active.is_(True),
                Category.is_active.is_(True),
                Catalog.is_active.is_(True),
            )
            .order_by(Service.name)
        )

        async with self._session_factory() as session:
            paginated_query, paging = await get_query_with_meta(session, query, page, page_size)

            rows = await session.execute(paginated_query)
            services = [ServiceEntity.model_validate(row) for row in rows.unique().all()]

            return Paginated[ServiceEntity](data=services, paging=paging)
