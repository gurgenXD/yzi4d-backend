import traceback
from dataclasses import dataclass
from typing import TYPE_CHECKING
from app.services.updater.types import UpdaterStatusType, UpdaterDataType


if TYPE_CHECKING:
    from logging import Logger

    from app.adapters.source import SourceAdapter
    from app.adapters.storage.updater import UpdaterAdapter


@dataclass
class RepoUpdaterService:
    """Сервис обновления репозитория."""

    _source: "SourceAdapter"
    _updater: "UpdaterAdapter"
    _logger: "Logger"

    async def update(self, data_type: UpdaterDataType) -> None:
        """Обновить данные."""
        self._logger.info("Start updating repository...")
        update_id = await self._updater.start(data_type=data_type)

        status = UpdaterStatusType.SUCCESS
        message = None
        try:
            match data_type:
                case UpdaterDataType.MAIN:
                    self._logger.info("Start updating specialists...")
                    await self.update_specialists()

                    self._logger.info("Start updating services with prices...")
                    await self.update_services_with_prices()

                    self._logger.info("Start updating catalogs with categories...")
                    await self.update_catalogs()
                case UpdaterDataType.IMAGES:
                    self._logger.info("Start updating images...")
                    await self.update_images()
        except Exception:
            status = UpdaterStatusType.FAILURE
            message = str(traceback.format_exc())
            self._logger.exception(f"Updating failed. Reason: {message}")

        await self._updater.finish(update_id, status, message)
        self._logger.info("Updating repository was finished.")

    async def update_specialists(self) -> None:
        """Обновить специалистов."""
        specialists = await self._source.get_specialists()
        await self._updater.save_specialists(specialists)

    async def update_services_with_prices(self) -> None:
        """Обновить услуги и цены."""
        services = await self._source.get_services_with_prices()
        await self._updater.save_services_with_prices(services)

    async def update_catalogs(self) -> None:
        """Обновить каталоги."""
        catalogs = await self._source.get_catalogs()
        await self._updater.save_catalogs(catalogs)

        for catalog in catalogs:
            content = await self._source.get_catalog_content(catalog.guid)
            await self._updater.save_categories(catalog.guid, content)

    async def update_images(self) -> None:
        """Обновить фотографии."""
        for guid in await self._updater.get_specialists_guids():
            image = await self._source.get_image(guid)
            await self._updater.save_image(guid, image)
