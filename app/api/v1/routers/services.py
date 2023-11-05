from fastapi import APIRouter

from app.adapters.storage.pagination.schemas import Paginated
from app.container import CONTAINER
from app.services.updater.types import CatalogType
from app.services.schemas.services import CategorySchema, ServiceSchema

TAG = "catalog"
PREFIX = f"/{TAG}"
PAGE_SIZE = 10

router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("/{catalog_type}/categories")
async def get_categories(catalog_type: CatalogType) -> list[CategorySchema]:
    """Получить категории услуг."""
    services_adapter = CONTAINER.services_adapter()

    match catalog_type:
        case CatalogType.MAIN:
            return await services_adapter.get_categories_with_services(CatalogType.MAIN)
        case _:
            return await services_adapter.get_categories(catalog_type)


@router.get("/{catalog_type}/categories/{category_id}")
async def get_services(catalog_type: CatalogType, category_id: int, page: int = 1) -> Paginated[ServiceSchema]:
    """Получить услуги."""
    services_adapter = CONTAINER.services_adapter()
    return await services_adapter.get_paginated(category_id, catalog_type, page, PAGE_SIZE)


@router.get("/{catalog_type}/categories/{category_id}/items/{item_id}")
async def get_service(catalog_type: CatalogType, _category_id: int, item_id: int) -> ServiceSchema:
    """Получить услугу."""
    adapter = CONTAINER.services_adapter()
    category_id = await adapter.convert_category_id(item_id, catalog_type)
    return await adapter.get(item_id, category_id, catalog_type)
