import operator
from dataclasses import dataclass

import httpx

from app.domain.entities.patients import PatientEntity, PatientFinishedVisitEntity, PatientPlannedVisitEntity


@dataclass
class PatientsAdapter:
    """Адаптер для получения данных пациента."""

    _host: str
    _timeout: float

    async def get_info(self, id_: str) -> "PatientEntity":
        """Получить информацию о пациентах."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self._host}/lk/GetPacientData", params={"PacientID": id_}, timeout=self._timeout,
            )
            return PatientEntity.model_validate(response.json()[0])

    async def get_planned_visits(self, id_: str) -> list["PatientPlannedVisitEntity"]:
        """Получить запланированные визиты."""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self._host}/lk/GetPlanned", params={"PacientID": id_}, timeout=self._timeout)
            return [PatientPlannedVisitEntity.model_validate(item) for item in response.json()]

    async def get_finished_visits(self, id_: str, type_: str) -> list["PatientFinishedVisitEntity"]:
        """Получить завершенных визиты."""
        filter_operator = operator.eq if type_ == "analyzes" else operator.ne

        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self._host}/lk/GetEMR", params={"PacientID": id_}, timeout=self._timeout)
            return [
                PatientFinishedVisitEntity.model_validate(item)
                for item in response.json()
                if filter_operator(item["researchType"], "Анализы")
            ]

    async def get_file(self, id_: str, file_path: str) -> str:
        """Получить файл."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self._host}/lk/GetProtocol",
                params={"PacientID": id_, "storagePath": file_path},
                timeout=self._timeout,
            )
            return response.json()[0]["Protocol"]
