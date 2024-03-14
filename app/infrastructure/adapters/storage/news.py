from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass
from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from app.domain.entities.news import NewsEntity
from app.domain.services.exceptions import NotFoundError
from app.infrastructure.adapters.storage.models import News


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class NewsAdapter:
    """Адаптер для доступа к данным новостей."""

    _session_factory: Callable[[], AbstractAsyncContextManager["AsyncSession"]]

    async def get_all(self) -> list["NewsEntity"]:
        """Получить все активные новости."""
        query = select(News).where(News.is_active.is_(True))

        async with self._session_factory() as session:
            rows = await session.execute(query)
            return [NewsEntity.model_validate(row) for row in rows.scalars()]

    async def get(self, id_: int) -> "NewsEntity":
        """Получить новость."""
        query = select(News).where(News.id == id_, News.is_active.is_(True))

        async with self._session_factory() as session:
            row = await session.execute(query)

            try:
                news = NewsEntity.model_validate(row.one()[0])
            except NoResultFound as exc:
                raise NotFoundError(f"Новость с {id_=} не найдена.") from exc

        return news
