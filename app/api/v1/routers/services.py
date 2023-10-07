from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.adapters.storage.pagination.schemas import Paginated
from app.container import CONTAINER
from app.services.updater.types import CatalogPageType
from app.services.schemas.services import CategorySchema, ServiceSchema

TAG = "services"
PREFIX = f"/{TAG}"
PAGE_SIZE = 10

router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("/categories")
async def get_categories(catalog_page: CatalogPageType) -> list[CategorySchema]:
    """Получить категории услуг."""
    services_adapter = CONTAINER.services_adapter()

    return await services_adapter.get_categories(catalog_page)


@router.get("/categories/{category_id}")
async def get_services(category_id: int, page: int = 1) -> Paginated[ServiceSchema]:
    """Получить услуги."""
    services_adapter = CONTAINER.services_adapter()
    return await services_adapter.get_paginated(category_id, page, PAGE_SIZE)


@router.get("/{id}")
async def get_service(id: str) -> "HTMLResponse":
    """Получить услугу."""
    adapter = CONTAINER.services_adapter()
    return await adapter.get(id=id)
