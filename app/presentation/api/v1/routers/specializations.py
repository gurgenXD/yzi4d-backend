from fastapi import APIRouter

from app.container import CONTAINER
from app.domain.entities.specializations import SpecializationEntity


TAG = "specializations"
PREFIX = f"/{TAG}"


router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("")
async def get_specializations() -> list[SpecializationEntity]:
    """Получить специализации."""
    adapter = CONTAINER.specializations_adapter()
    return await adapter.get_all()
