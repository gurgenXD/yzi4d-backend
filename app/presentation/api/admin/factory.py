from typing import TYPE_CHECKING

from sqladmin import Admin

from app.infrastructure.adapters.storage.db import engine
from app.infrastructure.settings.auth import AuthSettings
from app.infrastructure.settings.db import DatabaseSettings
from app.presentation.api.admin.auth import AdminAuth
from app.presentation.api.admin.routers.callbacks import CallbackAdmin
from app.presentation.api.admin.routers.consultations import ConsultationAdmin
from app.presentation.api.admin.routers.contacts import CityAdmin, DepartmentAdmin, OfficeAdmin
from app.presentation.api.admin.routers.documents import DocumentAdmin, DocumentCategoryAdmin
from app.presentation.api.admin.routers.vacancies import VacancyAdmin, VacancyCategoryAdmin
from app.presentation.api.admin.routers.news import NewsAdmin
from app.presentation.api.admin.routers.pages import PagesAdmin
from app.presentation.api.admin.routers.promotions import PromotionsAdmin
from app.presentation.api.admin.routers.services import ServiceAdmin, ServiceCatalogAdmin, ServiceCategoryAdmin
from app.presentation.api.admin.routers.specialists import (
    SpecialistAdmin,
    SpecialistCertificateAdmin,
    SpecializationAdmin,
)
from app.presentation.api.admin.routers.updates import UpdatesAdmin
from utils.constants import TEMPLATES_DIR


if TYPE_CHECKING:
    from fastapi import FastAPI

PREFIX = "/admin"


def create_app(app: "FastAPI") -> None:
    """Добавить роутеры админ-панели."""
    db_settings = DatabaseSettings()
    auth_settings = AuthSettings()

    authentication_backend = AdminAuth(settings=auth_settings)

    admin = Admin(
        app,
        engine.get_async(db_settings),
        base_url=PREFIX,
        title="Admin",
        templates_dir=str(TEMPLATES_DIR / "sqladmin"),
        authentication_backend=authentication_backend,
    )

    admin.add_view(SpecialistAdmin)
    admin.add_view(SpecializationAdmin)
    admin.add_view(SpecialistCertificateAdmin)
    admin.add_view(ServiceCategoryAdmin)
    admin.add_view(ServiceCatalogAdmin)
    admin.add_view(ServiceAdmin)
    admin.add_view(PromotionsAdmin)
    admin.add_view(CityAdmin)
    admin.add_view(OfficeAdmin)
    admin.add_view(DepartmentAdmin)
    admin.add_view(DocumentAdmin)
    admin.add_view(DocumentCategoryAdmin)
    admin.add_view(VacancyAdmin)
    admin.add_view(VacancyCategoryAdmin)
    admin.add_view(NewsAdmin)
    admin.add_view(PagesAdmin)
    admin.add_view(CallbackAdmin)
    admin.add_view(ConsultationAdmin)
    admin.add_view(UpdatesAdmin)
