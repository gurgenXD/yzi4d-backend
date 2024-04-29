from fastapi import APIRouter, Depends, Path, Query

from app.container import CONTAINER
from app.domain.entities.patients import (
    PatientChangePasswordEntity,
    PatientEntity,
    PatientFinishedVisitEntity,
    PatientPlannedVisitEntity,
)
from app.presentation.api.auth.dependecies import get_token


TAG = "patients"
PREFIX = f"/{TAG}"


router = APIRouter(prefix=PREFIX, tags=[TAG], dependencies=[Depends(get_token)])


@router.get("/{id}")
async def get_patient(id_: str = Path(alias="id")) -> PatientEntity:
    """Получить информацию о пациенте."""
    adapter = CONTAINER.patients_adapter()
    return await adapter.get_info(id_)


@router.get("/{id}/planned-visits")
async def get_planned_visits(id_: str = Path(alias="id")) -> list[PatientPlannedVisitEntity]:
    """Получить информацию о запланированных визитах пациента."""
    adapter = CONTAINER.patients_adapter()
    return await adapter.get_planned_visits(id_)


@router.get("/{id}/finished-visits")
async def get_finished_visits(
    id_: str = Path(alias="id"), type_: str = Query(alias="type")
) -> list[PatientFinishedVisitEntity]:
    """Получить информацию о завершенных визитах пациента."""
    adapter = CONTAINER.patients_adapter()
    return await adapter.get_finished_visits(id_, type_)


@router.get("/{id}/file")
async def get_file(file_path: str, id_: str = Path(alias="id")) -> str:
    """Получить файл."""
    adapter = CONTAINER.patients_adapter()
    return await adapter.get_file(id_, file_path)


@router.post("/{id}/change-password")
async def change_password(credentials: PatientChangePasswordEntity, id_: str = Path(alias="id")) -> None:
    """Сменить пароль."""
    print(id_)
    print(credentials)
    # TODO: доделать
