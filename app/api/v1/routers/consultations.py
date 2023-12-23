from fastapi import APIRouter

from app.container import CONTAINER
from app.services.schemas.consultations import ConsultationSchema


TAG = "consultations"
PREFIX = f"/{TAG}"


router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.post("")
async def create_consultation(consultation: ConsultationSchema) -> None:
    """Добавить заявку на онлайн консультацию."""
    adapter = CONTAINER.consultation_adapter()
    return await adapter.create(consultation)
