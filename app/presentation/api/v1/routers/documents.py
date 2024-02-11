from fastapi import APIRouter

from app.container import CONTAINER
from app.domain.services.schemas.documents import DocumentCategorySchema


TAG = "documents"
PREFIX = f"/{TAG}"


router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("")
async def get_documents() -> list[DocumentCategorySchema]:
    """Получить документы."""
    adapter = CONTAINER.documents_adapter()
    return await adapter.get_all()
