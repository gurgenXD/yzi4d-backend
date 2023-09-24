from dataclasses import dataclass

import httpx

from app.services.updater.schemas.services import CatalogSchema, CatalogItemSchema, ServiceExtSchema
from app.services.updater.schemas.specialists import SourceSpecialistSchema


@dataclass
class SourceAdapter:
    """Адаптер для получения данных источника."""

    _host: str
    _timeout: float

    async def get_specialists(self) -> list["SourceSpecialistSchema"]:
        """Получить всех специалистов."""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self._host}/doctor/GetDoctorList", timeout=self._timeout)
            return [SourceSpecialistSchema(**item) for item in response.json()]

    async def get_catalogs(self) -> list["CatalogSchema"]:
        """Получить каталоги."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self._host}/product/GetCatalogList", timeout=self._timeout
            )
            return [CatalogSchema(**item) for item in response.json()]

    async def get_catalog_content(self, guid: str) -> list["CatalogItemSchema"]:
        """Получить содержимое каталога."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self._host}/product/GetCatalogContentByID",
                params={"CatalogID": guid},
                timeout=self._timeout,
            )

        return [CatalogItemSchema(**item) for item in response.json()]

    async def get_services(self) -> list["ServiceExtSchema"]:
        """Получить услуги и цены."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self._host}/product/GetExtProductList", timeout=self._timeout
            )

        return [ServiceExtSchema(**item) for item in response.json()]
