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

    return TEMPLATES.TemplateResponse(  # type: ignore
        "contacts.html", {"request": request, "cities": cities}
    )


@router.get("/{id}", response_class=HTMLResponse)
async def get_contacts_item(request: Request, id: int) -> "HTMLResponse":
    """Получить филиал."""
    adapter = CONTAINER.contacts_adapter()
    contact_item = await adapter.get(id=id)

    return TEMPLATES.TemplateResponse(  # type: ignore
        "office.html", {"request": request, "contact_item": contact_item}
    )
