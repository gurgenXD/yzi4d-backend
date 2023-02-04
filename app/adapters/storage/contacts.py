from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.adapters.storage.models import City
from app.services.schemas.offices import CitySchema

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class ContactsAdapter:
    """Адаптер для доступа к данным контактов."""

    def __init__(
        self, session_factory: Callable[[], AbstractAsyncContextManager["AsyncSession"]]
    ) -> None:
        self._session_factory = session_factory
        self._city = City

    async def get_cities(self) -> list["CitySchema"]:
        """Получить все города."""

        query = select(self._city).options(joinedload(self._city.offices))

        async with self._session_factory() as session:
            rows = await session.execute(query)
            cities = [CitySchema.from_orm(row) for row in rows.unique().scalars()]

        return cities
