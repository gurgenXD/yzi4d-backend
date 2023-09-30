from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.api.templates import TEMPLATES
from app.container import CONTAINER


TAG = "services"
PREFIX = f"/{TAG}"
PAGE_SIZE = 10

router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("/category/{type_id}", response_class=HTMLResponse)
async def get_services(request: Request, type_id: str, page: int = 1) -> "HTMLResponse":
    """Получить услуги."""
    services_types_adapter = CONTAINER.services_types_adapter()

    paginated = await services_types_adapter.get_paginated(type_id, page, PAGE_SIZE)
    services_types = await services_types_adapter.get_all()

    return TEMPLATES.TemplateResponse(  # type: ignore
        "services.html",
        {"request": request, "services": paginated.data, "paging": paginated.paging, "services_types": services_types},
    )


@router.get("/{id}", response_class=HTMLResponse)
async def get_service(request: Request, id: str) -> "HTMLResponse":
    """Получить услугу."""
    adapter = CONTAINER.services_adapter()
    service = await adapter.get(id=id)

    return TEMPLATES.TemplateResponse("service.html", {"request": request, "service": service})  # type: ignore
