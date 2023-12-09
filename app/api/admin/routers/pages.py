from fastapi import Request
from sqladmin import ModelView

from app.adapters.storage.models.pages import Page
from app.api.admin.permissions import PermissionType


class PagesAdmin(ModelView, model=Page):
    """Статичные страницы в админ панели."""

    name = "Page"
    name_plural = "Pages"
    icon = "fa-solid fa-images"

    can_export = False

    column_list = ("id", "title", "url", "is_active")
    column_labels = {"id": "ID", "url": "URL", "title": "Title", "content": "Content", "is_active": "Is active"}

    def is_accessible(self, request: Request) -> bool:
        """Права на изменение."""
        if (permissions := request.session.get("permissions")) and PermissionType.ADMIN.value in permissions:
            return True
        return False

    def is_visible(self, request: Request) -> bool:
        """Права на просмотр."""
        if (permissions := request.session.get("permissions")) and PermissionType.ADMIN.value in permissions:
            return True
        return False
