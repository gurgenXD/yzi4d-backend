from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from app.adapters.storage.models import News
from app.services.exceptions import NotFoundError
from app.services.schemas.news import NewsSchema

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class NewsAdapter:
    """Адаптер для доступа к данным новостей."""

    def __init__(
        self, session_factory: Callable[[], AbstractAsyncContextManager["AsyncSession"]]
    ) -> None:
        self._session_factory = session_factory
        self._news = News

    async def get_all(self) -> list["NewsSchema"]:
        """Получить все активные новости."""
        query = select(self._news).where(self._news.is_active.is_(True))

        async with self._session_factory() as session:
            rows = await session.execute(query)
            return [NewsSchema.from_orm(row) for row in rows.scalars()]

    async def get(self, id: int) -> "NewsSchema":
        """Получить новость."""
        query = select(self._news).where(self._news.id == id, self._news.is_active.is_(True))

        async with self._session_factory() as session:
            row = await session.execute(query)

            try:
                news = NewsSchema.from_orm(row.one()[0])
            except NoResultFound as exc:
                message = f"Новость с {id=} не найдена."
                raise NotFoundError(message) from exc

        return news
