from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass
from typing import TYPE_CHECKING

from sqlalchemy import insert

from app.infrastructure.adapters.storage.models import Callback


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from app.domain.entities.callbacks import CallbackEntity


@dataclass
class CallbacksAdapter:
    """Адаптер для доступа к обратным звонкам."""

    _session_factory: Callable[[], AbstractAsyncContextManager["AsyncSession"]]

    async def create(self, callback: "CallbackEntity") -> None:
        """Создать заявку на обратный звонок."""
        query = insert(Callback).values(**callback.model_dump(), answered=False)

        async with self._session_factory() as session:
            await session.execute(query)
