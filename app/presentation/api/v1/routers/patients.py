from fastapi import APIRouter, Path

from app.container import CONTAINER
from app.domain.entities.patients import PatientEntity, PatientPlannedVisitEntity


TAG = "patients"
PREFIX = f"/{TAG}"


router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("/{id}")
async def get_patient(id_: str = Path(alias="id")) -> PatientEntity:
    """Получить информацию о пациенте."""
    adapter = CONTAINER.patients_adapter()
    return await adapter.get_info(id_)


@router.get("/{id}/planned-visits")
async def get_patient_planned_visits(id_: str = Path(alias="id")) -> list[PatientPlannedVisitEntity]:
    """Получить информацию о запланированных визитах пациента."""
    adapter = CONTAINER.patients_adapter()
    return await adapter.get_planned_visits(id_)
