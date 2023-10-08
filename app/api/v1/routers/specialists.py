from fastapi import APIRouter, status, Request

from app.adapters.storage.pagination.schemas import Paginated
from app.container import CONTAINER
from app.services.schemas.specialists import SpecialistSchema, SpecializationSchema
from app.services.schemas.services import ServiceSchema


TAG = "specialists"
PREFIX = f"/{TAG}"
PAGE_SIZE = 12


router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("/specializations")
async def get_specializations() -> list[SpecializationSchema]:
    """Получить специалистов."""
    adapter = CONTAINER.specialists_adapter()
    return await adapter.get_specializations()


@router.get("")
async def get_specialists(
    request: Request,
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
        base_url=request.base_url,
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
async def get_specialist(request: Request, id: int) -> SpecialistSchema:
    """Получить специалиста."""
    adapter = CONTAINER.specialists_adapter()
    return await adapter.get(base_url=request.base_url, id=id)


@router.get("/{id}/services", responses={status.HTTP_404_NOT_FOUND: {"detail": "Specialist not found"}})
async def get_specialist_services(id: int, page: int = 1) -> Paginated[ServiceSchema]:
    """Получить услуги специалиста."""
    adapter = CONTAINER.specialists_adapter()
    return await adapter.get_services(id=id, page=page, page_size=PAGE_SIZE)
