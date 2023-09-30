from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import TYPE_CHECKING, ClassVar

from sqlalchemy import insert, update

from app.adapters.storage.models import Update
from app.services.updater.types import UpdaterStatusType, UpdaterDataType


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class UpdaterAdapter:
    """Адаптер для доступа к данным обновления."""

    _session_factory: Callable[[], AbstractAsyncContextManager["AsyncSession"]]

    _updater: ClassVar = Update

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
