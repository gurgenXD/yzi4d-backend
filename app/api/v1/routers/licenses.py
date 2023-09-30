from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.api.templates import TEMPLATES
from app.container import CONTAINER


TAG = "licenses"
PREFIX = f"/{TAG}"


router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("", response_class=HTMLResponse)
async def get_licenses(request: Request) -> "HTMLResponse":
    """Получить лицензии."""
    adapter = CONTAINER.news_adapter()
    licenses = await adapter.get_all()

    return TEMPLATES.TemplateResponse("licenses.html", {"request": request, "licenses": licenses})  # type: ignore
