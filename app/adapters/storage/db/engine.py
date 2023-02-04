from typing import TYPE_CHECKING

from sqlalchemy import event
from sqlalchemy.ext.asyncio import create_async_engine

from app.settings.db import DatabaseSettings

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncEngine


def get_async() -> "AsyncEngine":
    """Получить асинхронный Engine для работы с БД."""
    settings = DatabaseSettings()

    engine = create_async_engine(
        url=settings.async_url,
        pool_size=settings.pool_size,
        max_overflow=settings.max_overflow,
        pool_timeout=settings.pool_timeout,
    )

    @event.listens_for(engine.sync_engine, "connect", insert=True)
    def set_search_path(dbapi_conn, _conn_record) -> None:
        """Проставить схему по умолчанию для соединения."""
        cursor = dbapi_conn.cursor()
        cursor.execute(f"SET search_path TO {settings.schema_};")
        cursor.execute("COMMIT;")
        cursor.close()

    return engine
