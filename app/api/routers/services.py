from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.api.templates import TEMPLATES
from app.container import CONTAINER

TAG = "services"
PREFIX = f"/{TAG}"


router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("/category/{type_id}", response_class=HTMLResponse)
async def get_services(request: Request, type_id: int) -> "HTMLResponse":
    """Получить услуги."""
    services_types_adapter = CONTAINER.services_types_adapter()

    service_type_current = await services_types_adapter.get(id=type_id)
    services_types = await services_types_adapter.get_all()

    return TEMPLATES.TemplateResponse(
        "services.html",
        {
            "request": request,
            "service_type_current": service_type_current,
            "services_types": services_types,
        },
    )


@router.get("/{id}", response_class=HTMLResponse)
async def get_service(request: Request, id: int) -> "HTMLResponse":
    """Получить услугу."""
    adapter = CONTAINER.services_adapter()
    service = await adapter.get(id=id)

    return TEMPLATES.TemplateResponse("service.html", {"request": request, "service": service})
