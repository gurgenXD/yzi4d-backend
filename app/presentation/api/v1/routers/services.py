from fastapi import APIRouter, Request

from app.container import CONTAINER
from app.domain.entities.services import CategoryEntity, ServiceEntity
from app.domain.services.updater.types import CatalogType
from app.infrastructure.adapters.storage.pagination.schemas import Paginated


TAG = "catalog"
PREFIX = f"/{TAG}"
PAGE_SIZE = 10

router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("/{catalog_type}/categories")
async def get_categories(
    request: Request, catalog_type: CatalogType, category_id: int | None = None, search_query: str | None = None,
) -> list[CategoryEntity]:
    """Получить категории услуг."""
    services_adapter = CONTAINER.services_adapter()

    match catalog_type:
        case CatalogType.MAIN:
            return await services_adapter.get_categories_with_services(request.base_url, CatalogType.MAIN)
        case _:
            return await services_adapter.get_categories(catalog_type, category_id, search_query)


@router.get("/{catalog_type}/services")
async def get_services(
    catalog_type: CatalogType, category_id: int | None = None, search_query: str | None = None, page: int = 1,
) -> Paginated[ServiceEntity]:
    """Получить услуги."""
    services_adapter = CONTAINER.services_adapter()
    return await services_adapter.get_paginated(catalog_type, category_id, search_query, page, PAGE_SIZE)


@router.get("/{catalog_type}/services/{item_id}")
async def get_service(catalog_type: CatalogType, item_id: int) -> ServiceEntity:
    """Получить услугу."""
    services_adapter = CONTAINER.services_adapter()
    category_id = await services_adapter.convert_category_id(item_id, catalog_type)
    return await services_adapter.get(item_id, category_id, catalog_type)
