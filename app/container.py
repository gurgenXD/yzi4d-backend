from contextlib import AbstractAsyncContextManager
from typing import TYPE_CHECKING

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Callable, Singleton

from app.adapters.source import SourceAdapter
from app.adapters.storage.analyzes import AnalyzesAdapter
from app.adapters.storage.contacts import ContactsAdapter
from app.adapters.storage.db import engine, session
from app.adapters.storage.news import NewsAdapter
from app.adapters.storage.pages import PagesAdapter
from app.adapters.storage.promotions import PromotionsAdapter
from app.adapters.storage.services import ServicesAdapter, ServiceTypeAdapter
from app.adapters.storage.specialists import SpecialistsAdapter, SpecializationAdapter
from app.services.updater.repo import RepoUdapterService
from app.settings.db import DatabaseSettings
from app.settings.service import ServiceSettings
from app.adapters.storage.updater import UpdaterAdapter


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession


class Container(DeclarativeContainer):
    """Контейнер зависимостей приложения."""

    db_settings: Singleton["DatabaseSettings"] = Singleton(DatabaseSettings)
    service_settings: Singleton["ServiceSettings"] = Singleton(ServiceSettings)

    async_engine: Singleton["AsyncEngine"] = Singleton(engine.get_async)
    session_ctx: Callable[AbstractAsyncContextManager["AsyncSession"]] = Callable(
        session.get_context, engine=async_engine.provided
    )

    specialists_adapter: Singleton["SpecialistsAdapter"] = Singleton(
        SpecialistsAdapter, session_factory=session_ctx.provider
    )
    specializations_adapter: Singleton["SpecializationAdapter"] = Singleton(
        SpecializationAdapter, session_factory=session_ctx.provider
    )
    analyzes_adapter: Singleton["AnalyzesAdapter"] = Singleton(
        AnalyzesAdapter, session_factory=session_ctx.provider
    )
    services_adapter: Singleton["ServicesAdapter"] = Singleton(
        ServicesAdapter, session_factory=session_ctx.provider
    )
    services_types_adapter: Singleton["ServiceTypeAdapter"] = Singleton(
        ServiceTypeAdapter, session_factory=session_ctx.provider
    )
    contacts_adapter: Singleton["ContactsAdapter"] = Singleton(
        ContactsAdapter, session_factory=session_ctx.provider
    )
    news_adapter: Singleton["NewsAdapter"] = Singleton(
        NewsAdapter, session_factory=session_ctx.provider
    )
    pages_adapter: Singleton["PagesAdapter"] = Singleton(
        PagesAdapter, session_factory=session_ctx.provider
    )
    promotions_adapter: Singleton["PromotionsAdapter"] = Singleton(
        PromotionsAdapter, session_factory=session_ctx.provider
    )
    updater_adapter: Singleton["UpdaterAdapter"] = Singleton(
        UpdaterAdapter, session_factory=session_ctx.provider
    )
    source_adapter: Singleton["SourceAdapter"] = Singleton(
        SourceAdapter, host=service_settings.provided.host_1c
    )

    repo_updater_service: Singleton["RepoUdapterService"] = Singleton(
        RepoUdapterService,
        source_adapter.provided,
        specialists_adapter.provided,
        updater_adapter.provided,
    )


CONTAINER = Container()
