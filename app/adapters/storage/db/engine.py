from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import create_async_engine

from app.settings.db import DatabaseSettings

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncEngine


def get_async() -> "AsyncEngine":
    """Получить асинхронный Engine для работы с БД."""
    settings = DatabaseSettings()

    return create_async_engine(
        url=settings.async_url,
        pool_size=settings.pool_size,
        max_overflow=settings.max_overflow,
        pool_timeout=settings.pool_timeout,
        connect_args={"server_settings": {"search_path": settings.schema_}},
    )
