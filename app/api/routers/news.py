from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.api.templates import TEMPLATES
from app.container import CONTAINER

TAG = "news"
PREFIX = f"/{TAG}"


router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("", response_class=HTMLResponse)
async def get_news(request: Request) -> "HTMLResponse":
    """Получить новости."""
    adapter = CONTAINER.news_adapter()
    news = await adapter.get_all()

    return TEMPLATES.TemplateResponse("news.html", {"request": request, "news": news})


@router.get("/{id}", response_class=HTMLResponse)
async def get_news_item(request: Request, id: int) -> "HTMLResponse":
    """Получить новость."""
    adapter = CONTAINER.news_adapter()
    news_item = await adapter.get(id=id)

    return TEMPLATES.TemplateResponse(
        "news_item.html", {"request": request, "news_item": news_item}
    )
