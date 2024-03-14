from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass
from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from app.domain.entities.pages import PageEntity
from app.domain.services.exceptions import NotFoundError
from app.infrastructure.adapters.storage.models import Page


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class PagesAdapter:
    """Адаптер для доступа к данным статичных страниц."""

    _session_factory: Callable[[], AbstractAsyncContextManager["AsyncSession"]]

    async def get(self, slug: str) -> "PageEntity":
        """Получить статичную страницу."""
        query = select(Page).where(Page.slug == slug, Page.is_active.is_(True))

        async with self._session_factory() as session:
            row = await session.execute(query)

            try:
                pages = PageEntity.model_validate(row.one()[0])
            except NoResultFound as exc:
                raise NotFoundError("Страница не найдена.") from exc

        return pages
