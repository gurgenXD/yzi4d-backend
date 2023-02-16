from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import select

from app.adapters.storage.models import Promotion
from app.services.schemas.promotions import PromotionSchema


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class PromotionsAdapter:
    """Адаптер для доступа к данным акций."""

    def __init__(
        self, session_factory: Callable[[], AbstractAsyncContextManager["AsyncSession"]]
    ) -> None:
        self._session_factory = session_factory
        self._promotion = Promotion

    async def get_all(self, *, for_main: bool) -> list["PromotionSchema"]:
        """Получить все активные акции."""
        query = select(self._promotion).where(
            self._promotion.date_end >= datetime.now(tz=timezone.utc).date()
        )

        if for_main:
            query = query.where(self._promotion.on_main.is_(True))

        async with self._session_factory() as session:
            rows = await session.execute(query)
            return [PromotionSchema.from_orm(row) for row in rows.scalars()]
