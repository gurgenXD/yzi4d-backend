from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from typing import TYPE_CHECKING
from datetime import datetime, timezone
from app.services.updater.types import UpdaterStatusType

from sqlalchemy import insert, update

from app.adapters.storage.models import Updater


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class UpdaterAdapter:
    """Адаптер для доступа к данным обновления."""

    def __init__(
        self, session_factory: Callable[[], AbstractAsyncContextManager["AsyncSession"]]
    ) -> None:
        self._session_factory = session_factory
        self._updater = Updater

    async def start(self) -> int:
        """Создать запись о начале обновления."""
        query = (
            insert(self._updater)
            .values(
                start_update=datetime.now(tz=timezone.utc),
                status=UpdaterStatusType.PROCESSING.value,
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
            .values(
                end_update=datetime.now(tz=timezone.utc), status=status.value, error_log=message
            )
        )

        async with self._session_factory() as session:
            await session.execute(query)
