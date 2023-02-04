from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncEngine


def get_factory(engine: "AsyncEngine") -> "sessionmaker":
    """Получить фабрику для создания асинхронных сессий."""
    return sessionmaker(
        bind=engine, class_=AsyncSession, autoflush=False, autocommit=False, expire_on_commit=True
    )


@asynccontextmanager
async def get_context(engine: "AsyncEngine") -> AsyncIterator["AsyncSession"]:
    """Контекстный менеджер для создания сессии."""
    async with get_factory(engine).begin() as session:
        yield session
