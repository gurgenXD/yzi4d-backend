from fastapi import APIRouter, Request

from app.container import CONTAINER
from app.domain.entities.promotions import PromotionEntity


TAG = "promotions"
PREFIX = f"/{TAG}"


router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("")
async def get_promotions(request: Request, *, for_main: bool = False) -> list[PromotionEntity]:
    """Получить акции."""
    adapter = CONTAINER.promotions_adapter()
    return await adapter.get_all(base_url=request.base_url, for_main=for_main)
