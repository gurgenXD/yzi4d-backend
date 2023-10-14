from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass
from typing import TYPE_CHECKING

from sqlalchemy import select

from app.adapters.storage.models import Document
from app.services.schemas.documents import DocumentSchema


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class DocumentAdapter:
    """Адаптер для доступа к данным документов."""

    _session_factory: Callable[[], AbstractAsyncContextManager["AsyncSession"]]

    async def get_all(self) -> list["DocumentSchema"]:
        """Получить все активные лицензии."""
        query = select(Document).where(Document.is_active.is_(True))

        async with self._session_factory() as session:
            rows = await session.execute(query)
            return [DocumentSchema.model_validate(row) for row in rows.scalars()]
