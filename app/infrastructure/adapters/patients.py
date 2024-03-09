import operator
from dataclasses import dataclass

import httpx

from app.domain.entities.patients import PatientEntity, PatientFinishedVisitEntity, PatientPlannedVisitEntity
from app.domain.services.exceptions import NotFoundError


@dataclass
class PatientsAdapter:
    """Адаптер для получения данных пациента."""

    _host: str
    _username: str
    _password: str
    _timeout: float

    @property
    def _auth(self) -> httpx.BasicAuth:
        """Аутентификация."""
        return httpx.BasicAuth(username=self._username, password=self._password)

    async def get_info(self, id_: str) -> "PatientEntity":
        """Получить информацию о пациентах."""
        async with httpx.AsyncClient(auth=self._auth) as client:
            response = await client.get(
                f"{self._host}/lk/GetPacientData", params={"PacientID": id_}, timeout=self._timeout,
            )

            try:
                return PatientEntity.model_validate(response.json())
            except ValueError as exc:
                message = f"Patient with id={id_} not found."
                raise NotFoundError(message) from exc

    async def get_planned_visits(self, id_: str) -> list["PatientPlannedVisitEntity"]:
        """Получить запланированные визиты."""
        async with httpx.AsyncClient(auth=self._auth) as client:
            response = await client.get(f"{self._host}/lk/GetPlanned", params={"PacientID": id_}, timeout=self._timeout)

            try:
                return [PatientPlannedVisitEntity.model_validate(item) for item in response.json()]
            except ValueError as exc:
                message = f"Patient with id={id_} not found."
                raise NotFoundError(message) from exc

    async def get_finished_visits(self, id_: str, type_: str) -> list["PatientFinishedVisitEntity"]:
        """Получить завершенных визиты."""
        filter_operator = operator.eq if type_ == "analyzes" else operator.ne

        async with httpx.AsyncClient(auth=self._auth) as client:
            response = await client.get(f"{self._host}/lk/GetEMR", params={"PacientID": id_}, timeout=self._timeout)

            try:
                return [
                    PatientFinishedVisitEntity.model_validate(item)
                    for item in response.json()
                    if filter_operator(item["researchType"], "Анализы")
                ]
            except TypeError as exc:
                message = f"Patient with id={id_} not found."
                raise NotFoundError(message) from exc

    async def get_file(self, id_: str, file_path: str) -> str:
        """Получить файл."""
        async with httpx.AsyncClient(auth=self._auth) as client:
            response = await client.get(
                f"{self._host}/lk/GetProtocol",
                params={"PacientID": id_, "storagePath": file_path},
                timeout=self._timeout,
            )

            if data := response.json().get("Protocol"):
                return data

            message = f"Patient with id={id_} not found."
            raise NotFoundError(message)
