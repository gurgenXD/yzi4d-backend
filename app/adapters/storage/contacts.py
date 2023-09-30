from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

from sqlalchemy import select
from sqlalchemy.orm import contains_eager

from app.adapters.storage.models import City, Office
from app.services.schemas.contacts import CitySchema


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class ContactsAdapter:
    """Адаптер для доступа к данным контактов."""

    _session_factory: Callable[[], AbstractAsyncContextManager["AsyncSession"]]

    _city: ClassVar = City
    _office: ClassVar = Office

    async def get_cities(self) -> list["CitySchema"]:
        """Получить все города с контактами."""
        query = (
            select(self._city)
            .join(self._office)
            .options(contains_eager(self._city.offices))
            .where(self._city.is_active.is_(True), self._office.is_active.is_(True))
        )

        async with self._session_factory() as session:
            rows = await session.execute(query)
            return [CitySchema.model_validate(row) for row in rows.unique().scalars()]
