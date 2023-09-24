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
    promotions = await adapter.get_all(for_main=False)

    return TEMPLATES.TemplateResponse(  # type: ignore
        "promotions.html", {"request": request, "promotions": promotions}
    )
