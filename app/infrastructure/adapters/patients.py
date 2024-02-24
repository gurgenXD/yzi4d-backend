from dataclasses import dataclass

import httpx

from app.domain.entities.patients import PatientEntity, PatientPlannedVisitEntity


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
