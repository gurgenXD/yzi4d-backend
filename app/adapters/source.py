from dataclasses import dataclass

import httpx

from app.services.updater.schemas.services import SourceServiceGroupSchema, SourceServiceSchema
from app.services.updater.schemas.specialists import SourceSpecialistSchema


@dataclass
class SourceAdapter:
    """Адаптер для получения данных источника."""

    _host: str

    async def get_specialists(self) -> list["SourceSpecialistSchema"]:
        """Получить всех специалистов."""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self._host}/doctor/GetDoctorList", timeout=60)
            return [SourceSpecialistSchema(**item) for item in response.json()]

    async def get_services_groups(self) -> list["SourceServiceGroupSchema"]:
        """Получить группы услуг."""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self._host}/product/GetProductGroups", timeout=60)
            return [SourceServiceGroupSchema(**item) for item in response.json()]

    async def get_services(self) -> list["SourceServiceSchema"]:
        """Получить услуги."""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self._host}/product/GetExtProductList", timeout=60)
            return [SourceServiceSchema(**item) for item in response.json()]
