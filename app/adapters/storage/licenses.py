from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

from sqlalchemy import select

from app.adapters.storage.models import License
from app.services.schemas.licenses import LicenseSchema


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class LicenseAdapter:
    """Адаптер для доступа к данным лицензий."""

    _session_factory: Callable[[], AbstractAsyncContextManager["AsyncSession"]]

    _license: ClassVar = License

    async def get_all(self) -> list["LicenseSchema"]:
        """Получить все активные лицензии."""
        query = select(self._license).where(self._license.is_active.is_(True))

        async with self._session_factory() as session:
            rows = await session.execute(query)
            return [LicenseSchema.from_orm(row) for row in rows.scalars()]
