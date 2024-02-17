from fastapi import APIRouter

from app.container import CONTAINER
from app.domain.entities.documents import DocumentCategoryEntity


TAG = "documents"
PREFIX = f"/{TAG}"


router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("")
async def get_documents() -> list[DocumentCategoryEntity]:
    """Получить документы."""
    adapter = CONTAINER.documents_adapter()
    return await adapter.get_all()
