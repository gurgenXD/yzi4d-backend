from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.api.templates import TEMPLATES
from app.container import CONTAINER


TAG = "services"
PREFIX = f"/{TAG}"


router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("", response_class=HTMLResponse)
async def get_services(request: Request) -> "HTMLResponse":
    """Получить услуги."""
    adapter = CONTAINER.services_adapter()
    services = await adapter.get_all(for_main=False)

    return TEMPLATES.TemplateResponse("services.html", {"request": request, "services": services})


@router.get("/{id}", response_class=HTMLResponse)
async def get_service(request: Request, id: int) -> "HTMLResponse":
    """Получить услугу."""
    adapter = CONTAINER.services_adapter()
    service = await adapter.get(id=id)

    return TEMPLATES.TemplateResponse("service.html", {"request": request, "service": service})
