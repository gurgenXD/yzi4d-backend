from fastapi import APIRouter

from app.container import CONTAINER
from app.domain.entities.contacts import CityEntity


TAG = "contacts"
PREFIX = f"/{TAG}"


router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("")
async def get_contacts() -> list[CityEntity]:
    """Получить контакты."""
    adapter = CONTAINER.contacts_adapter()
    return await adapter.get_cities()


@router.get("/offices")
async def get_offices() -> list[str]:
    """Получить филиалы."""
    adapter = CONTAINER.contacts_adapter()
    return await adapter.get_offices()
