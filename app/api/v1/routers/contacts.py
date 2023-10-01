from fastapi import APIRouter

from app.container import CONTAINER
from app.services.schemas.contacts import CitySchema


TAG = "contacts"
PREFIX = f"/{TAG}"


router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("")
async def get_contacts() -> list[CitySchema]:
    """Получить контакты."""
    adapter = CONTAINER.contacts_adapter()
    return await adapter.get_cities()