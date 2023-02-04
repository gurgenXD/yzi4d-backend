from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.api.templates import TEMPLATES
from app.container import CONTAINER

TAG = "promotions"
PREFIX = f"/{TAG}"


router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("", response_class=HTMLResponse)
async def get_promotions(request: Request) -> "HTMLResponse":
    """Получить акции."""
    adapter = CONTAINER.promotions_adapter()
    promotions = await adapter.get_all(on_main=False)

    return TEMPLATES.TemplateResponse(
        "promotions.html", {"request": request, "promotions": promotions}
    )


@router.get("/{id}", response_class=HTMLResponse)
async def get_promotion(request: Request, id: int) -> "HTMLResponse":
    """Получить акцию."""
    adapter = CONTAINER.promotions_adapter()
    promotion = await adapter.get(id=id)

    return TEMPLATES.TemplateResponse(
        "promotion.html", {"request": request, "promotion": promotion}
    )
