import operator
from dataclasses import dataclass

import httpx

from app.domain.entities.patients import PatientEntity, PatientFinishedVisitEntity, PatientPlannedVisitEntity
from app.domain.services.exceptions import CredentialsError, NotFoundError


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

    async def get_patient_id(self, username: str, password: str) -> str:
        """Получить ID пациента."""
        async with httpx.AsyncClient(auth=self._auth) as client:
            response = await client.post(
                f"{self._host}/lk/Authorization",
                params={"login": username, "password": password},
                timeout=self._timeout,
            )
            data = response.json()

            if not data["result"]:
                raise CredentialsError("Wrong credentials.")

            return data["idPacient"]

    async def get_info(self, id_: str) -> "PatientEntity":
        """Получить информацию о пациентах."""
        async with httpx.AsyncClient(auth=self._auth) as client:
            response = await client.get(
                f"{self._host}/lk/GetPacientData", params={"PacientID": id_}, timeout=self._timeout
            )

            if response.status_code == httpx.codes.NOT_FOUND:
                raise NotFoundError("Patient not found.")

            return PatientEntity.model_validate(response.json())

    async def get_planned_visits(self, id_: str) -> list["PatientPlannedVisitEntity"]:
        """Получить запланированные визиты."""
        async with httpx.AsyncClient(auth=self._auth) as client:
            response = await client.get(f"{self._host}/lk/GetPlanned", params={"PacientID": id_}, timeout=self._timeout)

            if response.status_code == httpx.codes.NOT_FOUND:
                raise NotFoundError("Patient not found.")

            return [PatientPlannedVisitEntity.model_validate(item) for item in response.json()]

    async def get_finished_visits(self, id_: str, type_: str) -> list["PatientFinishedVisitEntity"]:
        """Получить завершенных визиты."""
        filter_operator = operator.eq if type_ == "analyzes" else operator.ne

        async with httpx.AsyncClient(auth=self._auth) as client:
            response = await client.get(f"{self._host}/lk/GetEMR", params={"PacientID": id_}, timeout=self._timeout)

            if response.status_code == httpx.codes.NOT_FOUND:
                raise NotFoundError("Patient not found.")

            return [
                PatientFinishedVisitEntity.model_validate(item)
                for item in response.json()
                if filter_operator(item["researchType"], "Анализы")
            ]

    async def get_file(self, id_: str, file_path: str) -> str:
        """Получить файл."""
        async with httpx.AsyncClient(auth=self._auth) as client:
            response = await client.get(
                f"{self._host}/lk/GetProtocol",
                params={"PacientID": id_, "storagePath": file_path},
                timeout=self._timeout,
            )

            if response.status_code == httpx.codes.NOT_FOUND or not (data := response.json().get("Protocol")):
                raise NotFoundError("Patient not found.")

            return data

    async def generate_password(self, username: str) -> None:
        """Сгенерировать пароль."""
        async with httpx.AsyncClient(auth=self._auth) as client:
            response = await client.post(
                f"{self._host}/lk/GetNewUser", params={"login": username}, timeout=self._timeout
            )

            if not response.json().get("result"):
                raise NotFoundError("Patient not found.")

    async def change_password(self, id_: str, password: str, new_password: str) -> None:
        """Изменить пароль."""
        async with httpx.AsyncClient(auth=self._auth) as client:
            response = await client.post(
                f"{self._host}/lk/changePassword",
                params={"PacientID": id_, "password": password, "newpassword": new_password},
                timeout=self._timeout,
            )

            if not response.json().get("result"):
                raise CredentialsError("Wrong credentials.")
