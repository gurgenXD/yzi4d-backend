from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass
from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.orm import contains_eager

from app.domain.entities.documents import DocumentCategoryEntity
from app.infrastructure.adapters.storage.models import Document, DocumentCategory


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class DocumentsAdapter:
    """Адаптер для доступа к данным документов."""

    _session_factory: Callable[[], AbstractAsyncContextManager["AsyncSession"]]

    async def get_all(self) -> list["DocumentCategoryEntity"]:
        """Получить все активные документы."""
        query = (
            select(DocumentCategory)
            .join(Document)
            .options(contains_eager(DocumentCategory.documents))
            .where(DocumentCategory.is_active.is_(True), Document.is_active.is_(True))
        )

        async with self._session_factory() as session:
            rows = await session.execute(query)
            return [DocumentCategoryEntity.model_validate(row) for row in rows.unique().scalars()]
