from contextlib import AbstractAsyncContextManager
from typing import TYPE_CHECKING

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Callable, Object, Singleton
from loguru import logger

from app.domain.services.updater.repo import RepoUpdaterService
from app.infrastructure.adapters.source import SourceAdapter
from app.infrastructure.adapters.storage.consultations import ConsultationsAdapter
from app.infrastructure.adapters.storage.contacts import ContactsAdapter
from app.infrastructure.adapters.storage.db import engine, session
from app.infrastructure.adapters.storage.documents import DocumentAdapter
from app.infrastructure.adapters.storage.news import NewsAdapter
from app.infrastructure.adapters.storage.pages import PagesAdapter
from app.infrastructure.adapters.storage.promotions import PromotionsAdapter
from app.infrastructure.adapters.storage.services import ServicesAdapter
from app.infrastructure.adapters.storage.specialists import SpecialistsAdapter
from app.infrastructure.adapters.storage.updater import UpdaterAdapter
from app.infrastructure.settings.auth import AuthSettings
from app.infrastructure.settings.db import DatabaseSettings
from app.infrastructure.settings.server import ServerSettings
from app.infrastructure.settings.service import ServiceSettings


if TYPE_CHECKING:
    from logging import Logger

    from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession


class Container(DeclarativeContainer):
    """Контейнер зависимостей приложения."""

    db_settings: Singleton["DatabaseSettings"] = Singleton(DatabaseSettings)
    service_settings: Singleton["ServiceSettings"] = Singleton(ServiceSettings)
    server_settings: Singleton["ServerSettings"] = Singleton(ServerSettings)
    auth_settings: Singleton["AuthSettings"] = Singleton(AuthSettings)

    logger: Object["Logger"] = Object(logger)  # type: ignore

    async_engine: Singleton["AsyncEngine"] = Singleton(engine.get_async, db_settings.provided)
    session_ctx: Callable[AbstractAsyncContextManager["AsyncSession"]] = Callable(
        session.get_context, engine=async_engine.provided
    )

    specialists_adapter: Singleton["SpecialistsAdapter"] = Singleton(SpecialistsAdapter, session_ctx.provider)
    services_adapter: Singleton["ServicesAdapter"] = Singleton(ServicesAdapter, session_ctx.provider)
    contacts_adapter: Singleton["ContactsAdapter"] = Singleton(ContactsAdapter, session_ctx.provider)
    news_adapter: Singleton["NewsAdapter"] = Singleton(NewsAdapter, session_ctx.provider)
    documents_adapter: Singleton["DocumentAdapter"] = Singleton(DocumentAdapter, session_ctx.provider)
    pages_adapter: Singleton["PagesAdapter"] = Singleton(PagesAdapter, session_ctx.provider)
    promotions_adapter: Singleton["PromotionsAdapter"] = Singleton(PromotionsAdapter, session_ctx.provider)
    updater_adapter: Singleton["UpdaterAdapter"] = Singleton(UpdaterAdapter, session_ctx.provider, logger.provided)
    source_adapter: Singleton["SourceAdapter"] = Singleton(
        SourceAdapter, service_settings.provided.updater_host, service_settings.provided.timeout
    )
    consultation_adapter: Singleton["ConsultationsAdapter"] = Singleton(ConsultationsAdapter, session_ctx.provider)

    repo_updater_service: Singleton["RepoUpdaterService"] = Singleton(
        RepoUpdaterService, source_adapter.provided, updater_adapter.provided, logger.provided
    )


CONTAINER = Container()
