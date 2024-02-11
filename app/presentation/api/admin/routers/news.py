from fastapi import Request
from sqladmin import ModelView

from app.infrastructure.adapters.storage.models.news import News
from app.presentation.api.admin.permissions import PermissionType


class NewsAdmin(ModelView, model=News):
    """Новости в админ панели."""

    name = "News"
    name_plural = "News"
    icon = "fa-solid fa-newspaper"

    can_export = False

    column_list = ("id", "title", "preview", "created")
    column_labels = {
        "id": "ID",
        "title": "Title",
        "preview": "Preview",
        "description": "Description",
        "created": "Created",
        "photo": "Photo",
        "is_active": "Is active",
    }

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
