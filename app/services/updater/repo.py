import traceback
from dataclasses import dataclass
from typing import TYPE_CHECKING

from app.services.updater.types import UpdaterStatusType


if TYPE_CHECKING:
    from logging import Logger

    from app.adapters.source import SourceAdapter
    from app.adapters.storage.services import ServicesAdapter
    from app.adapters.storage.specialists import SpecialistsAdapter
    from app.adapters.storage.updater import UpdaterAdapter


@dataclass
class RepoUdapterService:
    """Сервис обновления репозитория."""

    _source: "SourceAdapter"
    _specialists: "SpecialistsAdapter"
    _updater: "UpdaterAdapter"
    _services: "ServicesAdapter"
    _logger: "Logger"

    async def update(self) -> None:
        """Обновить данные."""
        self._logger.info("Start updating repository...")
        update_id = await self._updater.start()

        status = UpdaterStatusType.SUCCESS
        message = None
        try:
            self._logger.info("Start updating specialists...")
            await self.update_specialists()

            self._logger.info("Start updating services groups...")
            await self.update_services_groups()

            self._logger.info("Start updating services...")
            await self.update_services()
        except Exception:
            status = UpdaterStatusType.FAILURE
            message = str(traceback.format_exc())
            self._logger.exception(f"Updating failed. Reason: {message}")

        await self._updater.finish(update_id, status, message)
        self._logger.info("Updating repository was finished.")

    async def update_specialists(self) -> None:
        """Обновить специалистов."""
        specialists = await self._source.get_specialists()
        await self._specialists.create_or_update(specialists)

    async def update_services_groups(self) -> None:
        """Обновить группы услуг."""
        services_groups = await self._source.get_services_groups()
        await self._services.create_or_update_groups(services_groups)

    async def update_services(self) -> None:
        """Обновить услуги."""
        services = await self._source.get_services()
        await self._services.create_or_update(services)
