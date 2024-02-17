from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass
from typing import TYPE_CHECKING

from sqlalchemy import select

from app.domain.entities.specializations import SpecializationEntity
from app.infrastructure.adapters.storage.models import Specialization


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class SpecializationsAdapter:
    """Адаптер для доступа к данным специализаций."""

    _session_factory: Callable[[], AbstractAsyncContextManager["AsyncSession"]]

    async def get_all(self) -> list["SpecializationEntity"]:
        """Получить специальности."""
        query = select(Specialization).where(Specialization.is_active.is_(True)).order_by(Specialization.name)

        async with self._session_factory() as session:
            rows = await session.execute(query)
            return [SpecializationEntity.model_validate(row) for row in rows.unique().scalars()]
