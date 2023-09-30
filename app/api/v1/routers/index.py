from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.api.templates import TEMPLATES
from app.container import CONTAINER


TAG = "index"
PREFIX = ""
SPECIALISTS_COUNT = 20


router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("/", response_class=HTMLResponse)
async def get_index(request: Request) -> "HTMLResponse":
    """Получить главную страницу."""
    specialists_adapter = CONTAINER.specialists_adapter()
    promotions_adapter = CONTAINER.promotions_adapter()
    cities_adapter = CONTAINER.contacts_adapter()

    paginated = await specialists_adapter.get_paginated(for_main=True, page=1, page_size=SPECIALISTS_COUNT)

    promotions = await promotions_adapter.get_all(for_main=True)

    cities = await cities_adapter.get_cities()

    return TEMPLATES.TemplateResponse(  # type: ignore
        "index.html", {"request": request, "specialists": paginated.data, "promotions": promotions, "cities": cities}
    )
