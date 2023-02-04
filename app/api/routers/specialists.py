from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.api.templates import TEMPLATES
from app.container import CONTAINER

TAG = "specialists"
PREFIX = f"/{TAG}"


router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("", response_class=HTMLResponse)
async def get_specialists(request: Request) -> "HTMLResponse":
    """Получить специалистов."""
    adapter = CONTAINER.specialists_adapter()
    specialists = await adapter.get_all(on_main=False)

    return TEMPLATES.TemplateResponse(
        "specialists.html", {"request": request, "specialists": specialists}
    )


@router.get("/{id}", response_class=HTMLResponse)
async def get_specialist(request: Request, id: int) -> "HTMLResponse":
    """Получить специалиста."""
    adapter = CONTAINER.specialists_adapter()
    specialist = await adapter.get(id=id)

    return TEMPLATES.TemplateResponse(
        "specialist.html", {"request": request, "specialist": specialist}
    )
