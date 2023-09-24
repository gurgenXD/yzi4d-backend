from fastapi import APIRouter

from app.container import CONTAINER
from app.services.schemas.news import NewsSchema


TAG = "news"
PREFIX = f"/{TAG}"


router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("")
async def get_news() -> list[NewsSchema]:
    """Получить новости."""
    adapter = CONTAINER.news_adapter()
    return await adapter.get_all()


@router.get("/{id}")
async def get_news_item(id: int) -> NewsSchema:
    """Получить новость."""
    adapter = CONTAINER.news_adapter()
    return await adapter.get(id=id)
