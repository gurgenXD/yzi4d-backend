from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass
from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.orm import contains_eager

from app.domain.services.schemas.documents import DocumentCategorySchema
from app.infrastructure.adapters.storage.models import Document, DocumentCategory


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class DocumentAdapter:
    """Адаптер для доступа к данным документов."""

    _session_factory: Callable[[], AbstractAsyncContextManager["AsyncSession"]]

    async def get_all(self) -> list["DocumentCategorySchema"]:
        """Получить все активные документы."""
        query = (
            select(DocumentCategory)
            .join(Document)
            .options(contains_eager(DocumentCategory.documents))
            .where(DocumentCategory.is_active.is_(True), Document.is_active.is_(True))
        )

        async with self._session_factory() as session:
            rows = await session.execute(query)
            return [DocumentCategorySchema.model_validate(row) for row in rows.unique().scalars()]
