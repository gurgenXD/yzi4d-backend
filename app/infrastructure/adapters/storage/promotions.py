from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import select

from app.domain.entities.promotions import PromotionEntity
from app.infrastructure.adapters.storage.models import Promotion


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class PromotionsAdapter:
    """Адаптер для доступа к данным акций."""

    _session_factory: Callable[[], AbstractAsyncContextManager["AsyncSession"]]

    async def get_all(self, *, base_url: str, for_main: bool) -> list["PromotionEntity"]:
        """Получить все активные акции."""
        current_date = datetime.now(tz=UTC).date()
        query = select(Promotion).where(Promotion.date_start <= current_date, Promotion.date_end >= current_date)

        if for_main:
            query = query.where(Promotion.on_main.is_(True))

        async with self._session_factory() as session:
            rows = await session.execute(query)

            promotions: list["PromotionEntity"] = []
            for row in rows.scalars():
                promotion = PromotionEntity.model_validate(row)
                promotion.photo = f"{base_url}media/promotions/{row.photo.name}" if row.photo else None
                promotions.append(promotion)

        return promotions
