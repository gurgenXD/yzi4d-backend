import requests

from app.services.updater.schemas.specialists import SourceSpecialistSchema


class SourceAdapter:
    """Адаптер для получения данных источника."""

    def __init__(self, host: str) -> None:
        self._host = host

    def get_specialists(self) -> list["SourceSpecialistSchema"]:
        """Получить всех специалистов."""
        response = requests.get(f"{self._host}/doctor/GetDoctorList", timeout=60)
        return [SourceSpecialistSchema(**item) for item in response.json()]
