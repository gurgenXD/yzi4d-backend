from fastapi import APIRouter, Path

from app.container import CONTAINER
from app.domain.entities.news import NewsEntity


TAG = "news"
PREFIX = f"/{TAG}"


router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("")
async def get_news() -> list[NewsEntity]:
    """Получить новости."""
    adapter = CONTAINER.news_adapter()
    return await adapter.get_all()


@router.get("/{id}")
async def get_news_item(id_: int = Path(alias="id")) -> NewsEntity:
    """Получить новость."""
    adapter = CONTAINER.news_adapter()
    return await adapter.get(id_=id_)
