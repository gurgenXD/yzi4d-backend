from fastapi import APIRouter, status

from app.adapters.storage.pagination.schemas import Paginated
from app.container import CONTAINER
from app.services.schemas.specialists import SpecialistSchema


TAG = "specialists"
PREFIX = f"/{TAG}"
PAGE_SIZE = 12


router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("")
async def get_specialists(
    can_online: bool = False,
    can_adult: bool = False,
    can_child: bool = False,
    search_query: str | None = None,
    specialization_id: int | None = None,
    page: int = 1,
) -> Paginated[SpecialistSchema]:
    """Получить специалистов."""
    adapter = CONTAINER.specialists_adapter()

    return await adapter.get_paginated(
        for_main=False,
        can_online=can_online,
        can_adult=can_adult,
        can_child=can_child,
        search_query=search_query,
        specialization_id=specialization_id,
        page=page,
        page_size=PAGE_SIZE,
    )


@router.get("/{id}", responses={status.HTTP_404_NOT_FOUND: {"detail": "Specialist not found"}})
async def get_specialist(id: str) -> SpecialistSchema:
    """Получить специалиста."""
    adapter = CONTAINER.specialists_adapter()
    return await adapter.get(id=id)
