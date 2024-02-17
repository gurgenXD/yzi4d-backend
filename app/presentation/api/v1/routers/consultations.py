from fastapi import APIRouter

from app.container import CONTAINER
from app.domain.entities.consultations import ConsultationEntity


TAG = "consultations"
PREFIX = f"/{TAG}"


router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.post("")
async def create_consultation(consultation: ConsultationEntity) -> None:
    """Добавить заявку на онлайн консультацию."""
    adapter = CONTAINER.consultation_adapter()
    return await adapter.create(consultation)
