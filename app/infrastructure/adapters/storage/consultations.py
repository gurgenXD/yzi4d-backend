from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass
from typing import TYPE_CHECKING

from sqlalchemy import insert

from app.infrastructure.adapters.storage.models import Consultation


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from app.domain.entities.consultations import ConsultationEntity


@dataclass
class ConsultationsAdapter:
    """Адаптер для доступа к данным консультаций."""

    _session_factory: Callable[[], AbstractAsyncContextManager["AsyncSession"]]

    async def create(self, consultation: "ConsultationEntity") -> None:
        """Создать заявку на консультацию."""
        query = insert(Consultation).values(**consultation.model_dump())

        async with self._session_factory() as session:
            await session.execute(query)
