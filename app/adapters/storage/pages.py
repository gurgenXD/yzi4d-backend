from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass
from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from app.adapters.storage.models import Page
from app.services.exceptions import NotFoundError
from app.services.schemas.pages import PageSchema


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class PagesAdapter:
    """Адаптер для доступа к данным статичных страниц."""

    _session_factory: Callable[[], AbstractAsyncContextManager["AsyncSession"]]

    async def get(self, slug: str) -> "PageSchema":
        """Получить статичную страницу."""
        query = select(Page).where(Page.slug == slug, Page.is_active.is_(True))

        async with self._session_factory() as session:
            row = await session.execute(query)

            try:
                pages = PageSchema.model_validate(row.one()[0])
            except NoResultFound as exc:
                message = "Страница не найдена."
                raise NotFoundError(message) from exc

        return pages
