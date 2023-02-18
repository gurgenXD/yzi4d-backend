from typing import TYPE_CHECKING
from app.services.updater.types import UpdaterStatusType
import traceback


if TYPE_CHECKING:
    from app.adapters.source import SourceAdapter
    from app.adapters.storage.specialists import SpecialistsAdapter
    from app.adapters.storage.updater import UpdaterAdapter


class RepoUdapterService:
    """Сервис обновления репозитория."""

    def __init__(
        self, source: "SourceAdapter", specialist: "SpecialistsAdapter", updater: "UpdaterAdapter"
    ) -> None:
        self._source = source
        self._specialist = specialist
        self._updater = updater

    async def update(self) -> None:
        """Обновить данные."""
        update_id = await self._updater.start()

        status = UpdaterStatusType.SUCCESS
        message = None
        try:
            specialists = await self._source.get_specialists()

            await self._specialist.create_or_update(specialists)
        except Exception:
            status = UpdaterStatusType.FAILURE
            message = str(traceback.format_exc())

        await self._updater.finish(update_id, status, message)
