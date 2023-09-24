from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.api.templates import TEMPLATES
from app.container import CONTAINER


TAG = "pages"
PREFIX = f"/{TAG}"


router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("/{slug}", response_class=HTMLResponse)
async def get_page(request: Request, slug: str) -> "HTMLResponse":
    """Получить страницу."""
    adapter = CONTAINER.pages_adapter()
    page = await adapter.get(slug=slug)

    return TEMPLATES.TemplateResponse(  # type: ignore
        "page.html", {"request": request, "page": page}
    )
