from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.api.templates import TEMPLATES
from app.container import CONTAINER


TAG = "contacts"
PREFIX = f"/{TAG}"


router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("", response_class=HTMLResponse)
async def get_contacts(request: Request) -> "HTMLResponse":
    """Получить контакты."""
    adapter = CONTAINER.contacts_adapter()
    cities = await adapter.get_cities()

    return TEMPLATES.TemplateResponse("contacts.html", {"request": request, "cities": cities})
