from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.api.templates import TEMPLATES

TAG = "index"
PREFIX = ""


router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("/", response_class=HTMLResponse)
async def get_index(request: Request) -> "HTMLResponse":
    """Получить главную страницу."""
    return TEMPLATES.TemplateResponse("index.html", {"request": request})
