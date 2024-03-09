from dataclasses import dataclass

import httpx

from app.domain.services.updater.schemas.services import CatalogItemSchema, CatalogSchema, ServiceExtSchema
from app.domain.services.updater.schemas.specialists import SourceSpecialistSchema, SpecialistImageSchema


@dataclass
class SourceAdapter:
    """Адаптер для получения данных источника."""

    _host: str
    _username: str
    _password: str
    _timeout: float

    @property
    def _auth(self) -> httpx.BasicAuth:
        """Аутентификация."""
        return httpx.BasicAuth(username=self._username, password=self._password)

    async def get_specialists(self) -> list["SourceSpecialistSchema"]:
        """Получить всех специалистов."""
        async with httpx.AsyncClient(auth=self._auth) as client:
            response = await client.get(f"{self._host}/doctor/GetDoctorList", timeout=self._timeout)
            return [SourceSpecialistSchema(**item) for item in response.json()]

    async def get_catalogs(self) -> list["CatalogSchema"]:
        """Получить каталоги."""
        async with httpx.AsyncClient(auth=self._auth) as client:
            response = await client.get(f"{self._host}/product/GetCatalogList", timeout=self._timeout)
            return [CatalogSchema(**item) for item in response.json()]

    async def get_catalog_content(self, guid: str) -> list["CatalogItemSchema"]:
        """Получить содержимое каталога."""
        async with httpx.AsyncClient(auth=self._auth) as client:
            response = await client.get(
                f"{self._host}/product/GetCatalogContentByID", params={"CatalogID": guid}, timeout=self._timeout,
            )

        return [CatalogItemSchema(**item) for item in response.json()]

    async def get_services_with_prices(self) -> list["ServiceExtSchema"]:
        """Получить услуги и цены."""
        async with httpx.AsyncClient(auth=self._auth) as client:
            response = await client.get(f"{self._host}/product/GetExtProductList", timeout=self._timeout)

        return [ServiceExtSchema(**item) for item in response.json()]

    async def get_image(self, guid: str) -> "SpecialistImageSchema":
        """Получить фотографию."""
        async with httpx.AsyncClient(auth=self._auth) as client:
            response = await client.get(
                f"{self._host}/doctor/GetFotoDoctorById", params={"DoctorID": guid}, timeout=self._timeout,
            )
            return SpecialistImageSchema(**response.json()[0])
