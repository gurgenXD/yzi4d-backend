from fastapi import Request
from sqladmin import ModelView

from app.adapters.storage.models.documents import Document, DocumentCategory
from app.api.admin.permissions import PermissionType


class DocumentAdmin(ModelView, model=Document):
    """Документы в админ панели."""

    name = "Document"
    name_plural = "Documents"
    icon = "fa-solid fa-file-contract"

    can_export = False

    column_list = ("id", "name", "link", "is_active")
    column_details_exclude_list = ("category_id",)
    column_labels = {"id": "ID", "name": "Name", "link": "Link", "is_active": "Is active", "category": "Category"}

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


class DocumentCategoryAdmin(ModelView, model=DocumentCategory):
    """Категории документы в админ панели."""

    name = "Category"
    name_plural = "Categories"
    icon = "fa-solid fa-folder-tree"

    can_export = False

    column_list = ("id", "name", "position", "is_active")
    column_details_exclude_list = ("documents",)
    column_labels = {"id": "ID", "name": "Name", "position": "Position", "is_active": "Is active"}

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
