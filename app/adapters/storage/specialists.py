from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

from sqlalchemy import or_, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import contains_eager

from app.adapters.storage.models import Specialist, Specialization
from app.adapters.storage.pagination.query import get_query_with_meta
from app.adapters.storage.pagination.schemas import Paginated
from app.services.exceptions import NotFoundError
from app.services.schemas.specialists import SpecialistSchema


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class SpecialistsAdapter:
    """Адаптер для доступа к данным специалистов."""

    _session_factory: Callable[[], AbstractAsyncContextManager["AsyncSession"]]

    _specialist: ClassVar = Specialist
    _specialization: ClassVar = Specialization

    async def get_paginated(
        self,
        *,
        for_main: bool,
        can_online: bool = False,
        can_adult: bool = False,
        can_child: bool = False,
        search_query: str | None = None,
        specialization_id: str | None = None,
        page: int = 1,
        page_size: int = 1,
    ) -> Paginated[SpecialistSchema]:
        """Получить всех активных специалистов."""
        query = (
            select(self._specialist.id).where(self._specialist.is_active.is_(True)).order_by(self._specialist.surname)
        )

        if for_main:
            query = query.where(self._specialist.on_main.is_(True))

        if can_online:
            query = query.where(self._specialist.can_online.is_(True))

        if can_adult:
            query = query.where(self._specialist.can_adult.is_(True))

        if can_child:
            query = query.where(self._specialist.can_child.is_(True))

        if search_query:
            search_query = search_query.strip()
            query = query.where(
                or_(
                    self._specialist.surname.ilike(f"%{search_query}%"),
                    self._specialist.name.ilike(f"%{search_query}%"),
                )
            )

        if specialization_id:
            query = query.where(self._specialization.id == specialization_id)

        async with self._session_factory() as session:
            paginated_query, paging = await get_query_with_meta(session, query, page, page_size)

            subquery = paginated_query.subquery()
            join_query = (
                select(self._specialist)
                .join(subquery, self._specialist.id == subquery.c.id)
                .join(self._specialist.specializations, isouter=True)
                .join(self._specialist.certificates, isouter=True)
                .options(
                    contains_eager(self._specialist.specializations), contains_eager(self._specialist.certificates)
                )
            )

            rows = await session.execute(join_query)
            specialists = [SpecialistSchema.model_validate(row) for row in rows.unique().scalars()]

            return Paginated[SpecialistSchema](data=specialists, paging=paging)

    async def get(self, id: int) -> "SpecialistSchema":
        """Получить специалиста."""
        query = (
            select(self._specialist)
            .join(self._specialist.specializations, isouter=True)
            .join(self._specialist.certificates, isouter=True)
            .options(contains_eager(self._specialist.specializations), contains_eager(self._specialist.certificates))
            .where(self._specialist.id == id, self._specialist.is_active.is_(True))
        )

        async with self._session_factory() as session:
            row = await session.execute(query)

            try:
                specialist = SpecialistSchema.model_validate(row.unique().one()[0])
            except NoResultFound as exc:
                message = f"Специалист с {id=} не найден."
                raise NotFoundError(message) from exc

        return specialist
