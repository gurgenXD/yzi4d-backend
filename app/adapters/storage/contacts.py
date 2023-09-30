from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload

from app.adapters.storage.models import City
from app.services.exceptions import NotFoundError
from app.services.schemas.offices import CitySchema


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class ContactsAdapter:
    """Адаптер для доступа к данным контактов."""

    _session_factory: Callable[[], AbstractAsyncContextManager["AsyncSession"]]

    _city: ClassVar = City

    async def get_cities(self) -> list["CitySchema"]:
        """Получить все города."""
        query = select(self._city).options(joinedload(self._city.offices))

        async with self._session_factory() as session:
            rows = await session.execute(query)
            return [CitySchema.mode(row) for row in rows.unique().scalars()]

    async def get(self, id: int) -> "CitySchema":
        """Получить филиал."""
        query = select(self._city).where(self._city == id)

        async with self._session_factory() as session:
            row = await session.execute(query)

            try:
                office = CitySchema.model_validate(row.one()[0])
            except NoResultFound as exc:
                message = f"Филиал с {id=} не найден."
                raise NotFoundError(message) from exc

        return office
