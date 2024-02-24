from contextlib import AbstractAsyncContextManager
from typing import TYPE_CHECKING

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Callable, Object, Provider, Singleton
from loguru import logger

from app.domain.services.updater.repo import RepoUpdaterService
from app.infrastructure.adapters.patients import PatientsAdapter
from app.infrastructure.adapters.source import SourceAdapter
from app.infrastructure.adapters.storage.consultations import ConsultationsAdapter
from app.infrastructure.adapters.storage.contacts import ContactsAdapter
from app.infrastructure.adapters.storage.db import engine, session
from app.infrastructure.adapters.storage.documents import DocumentsAdapter
from app.infrastructure.adapters.storage.news import NewsAdapter
from app.infrastructure.adapters.storage.pages import PagesAdapter
from app.infrastructure.adapters.storage.promotions import PromotionsAdapter
from app.infrastructure.adapters.storage.services import ServicesAdapter
from app.infrastructure.adapters.storage.specialists import SpecialistsAdapter
from app.infrastructure.adapters.storage.specializations import SpecializationsAdapter
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

    db_settings: Provider["DatabaseSettings"] = Singleton(DatabaseSettings)
    service_settings: Provider["ServiceSettings"] = Singleton(ServiceSettings)
    server_settings: Provider["ServerSettings"] = Singleton(ServerSettings)
    auth_settings: Provider["AuthSettings"] = Singleton(AuthSettings)

    logger: Provider["Logger"] = Object(logger)

    async_engine: Provider["AsyncEngine"] = Singleton(engine.get_async, db_settings.provided)
    session_ctx: Provider[AbstractAsyncContextManager["AsyncSession"]] = Callable(
        session.get_context, engine=async_engine.provided,
    )

    specialists_adapter: Provider["SpecialistsAdapter"] = Singleton(SpecialistsAdapter, session_ctx.provider)
    specializations_adapter: Provider["SpecializationsAdapter"] = Singleton(
        SpecializationsAdapter, session_ctx.provider,
    )
    services_adapter: Provider["ServicesAdapter"] = Singleton(ServicesAdapter, session_ctx.provider)
    contacts_adapter: Provider["ContactsAdapter"] = Singleton(ContactsAdapter, session_ctx.provider)
    news_adapter: Provider["NewsAdapter"] = Singleton(NewsAdapter, session_ctx.provider)
    documents_adapter: Provider["DocumentsAdapter"] = Singleton(DocumentsAdapter, session_ctx.provider)
    pages_adapter: Provider["PagesAdapter"] = Singleton(PagesAdapter, session_ctx.provider)
    promotions_adapter: Provider["PromotionsAdapter"] = Singleton(PromotionsAdapter, session_ctx.provider)
    updater_adapter: Provider["UpdaterAdapter"] = Singleton(UpdaterAdapter, session_ctx.provider, logger.provided)
    source_adapter: Provider["SourceAdapter"] = Singleton(
        SourceAdapter, service_settings.provided.updater_host, service_settings.provided.updater_timeout,
    )
    consultation_adapter: Provider["ConsultationsAdapter"] = Singleton(ConsultationsAdapter, session_ctx.provider)
    patients_adapter: Provider["PatientsAdapter"] = Singleton(
        PatientsAdapter, service_settings.provided.profile_host, service_settings.provided.profile_timeout,
    )

    repo_updater_service: Provider["RepoUpdaterService"] = Singleton(
        RepoUpdaterService, source_adapter.provided, updater_adapter.provided, logger.provided,
    )


CONTAINER = Container()
