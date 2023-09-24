from typing import TYPE_CHECKING

from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend

from app.adapters.storage.db import engine
from app.api.admin.routers.callbacks import CallbackAdmin
from app.api.admin.routers.documents import DocumentAdmin, DocumentCategoryAdmin
from app.api.admin.routers.news import NewsAdmin
from app.api.admin.routers.contacts import CityAdmin, OfficeAdmin, DepartmentAdmin
from app.api.admin.routers.pages import PagesAdmin
from app.api.admin.routers.promotions import PromotionsAdmin

from app.api.admin.routers.services import ServiceAdmin, ServiceCategoryAdmin, ServiceCatalogAdmin
from app.api.admin.routers.specialists import (
    SpecialistAdmin,
    SpecialistCertificateAdmin,
    SpecializationAdmin,
)
from app.api.admin.routers.updates import UpdatesAdmin
from app.settings.db import DatabaseSettings
from utils.constants import TEMPLATES_DIR


if TYPE_CHECKING:
    from fastapi import FastAPI

PREFIX = "/admin"


def create_app(app: "FastAPI") -> None:
    """Добавить роутеры админ-панели."""
    # authentication_backend = AdminAuth(secret_key="...")  # noqa: S106
    settings = DatabaseSettings()

    admin = Admin(
        app,
        engine.get_async(settings),
        base_url=PREFIX,
        title="Admin",
        templates_dir=str(TEMPLATES_DIR / "sqladmin"),
        # authentication_backend=authentication_backend,
    )

    admin.add_view(SpecialistAdmin)
    admin.add_view(SpecializationAdmin)
    admin.add_view(SpecialistCertificateAdmin)
    admin.add_view(ServiceAdmin)
    admin.add_view(ServiceCategoryAdmin)
    admin.add_view(ServiceCatalogAdmin)
    admin.add_view(PromotionsAdmin)
    admin.add_view(CityAdmin)
    admin.add_view(OfficeAdmin)
    admin.add_view(DepartmentAdmin)
    admin.add_view(DocumentAdmin)
    admin.add_view(DocumentCategoryAdmin)
    admin.add_view(NewsAdmin)
    admin.add_view(PagesAdmin)
    admin.add_view(CallbackAdmin)
    admin.add_view(UpdatesAdmin)


class AdminAuth(AuthenticationBackend):
    """Реализация аутентификации."""

    async def login(self, request: Request) -> bool:
        """Вход."""
        request.session.update({"token": "..."})
        return True

    async def logout(self, request: Request) -> bool:
        """Выход."""
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> RedirectResponse | None:
        """Аутентификация."""
        if "token" not in request.session:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

        return None
