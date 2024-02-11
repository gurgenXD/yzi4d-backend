from fastapi import Request
from sqladmin import ModelView

from app.infrastructure.adapters.storage.models.services import Catalog, Category, Service
from app.presentation.api.admin.permissions import PermissionType


class ServiceAdmin(ModelView, model=Service):
    """Услуги в админ панели."""

    name = "Service"
    name_plural = "Services"
    icon = "fa-solid fa-syringe"
    page_size = 20
    page_size_options = [20, 50, 100]

    can_edit = False
    can_create = False
    can_delete = False
    can_export = False

    column_list = ("id", "name", "is_active")
    column_sortable_list = ("name", "id")
    column_details_exclude_list = ("specialists_services",)
    column_labels = {
        "id": "ID",
        "guid": "GUID",
        "name": "Name",
        "short_description": "Short description",
        "description": "Description",
        "preparation": "Preparation",
        "ready_from": "Ready from",
        "ready_to": "Ready to",
        "is_active": "Is active",
        "categories": "Categories",
    }
    column_default_sort = [("name", False)]
    column_searchable_list = ("name", "id", "guid")

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


class ServiceCategoryAdmin(ModelView, model=Category):
    """Категории услуг в админ панели."""

    name = "Service category"
    name_plural = "Categories"
    icon = "fa-solid fa-folder-tree"

    can_create = False
    can_delete = False
    can_export = False

    column_list = ("id", "name", "parent", "catalog", "is_active")
    column_sortable_list = ("name", "id")
    column_details_exclude_list = ("parent_id", "catalog_id", "services")
    form_columns = ("icon",)
    column_labels = {
        "id": "ID",
        "guid": "GUID",
        "icon": "Icon",
        "name": "Name",
        "is_active": "Is active",
        "children": "Children",
        "parent": "Parent",
        "catalog": "Catalog",
        "catalog.name": "Catalog name",
    }
    column_default_sort = [("name", False)]
    column_searchable_list = ("name", "id", "guid", "catalog.name")

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


class ServiceCatalogAdmin(ModelView, model=Catalog):
    """Каталоги услуг в админ панели."""

    name = "Catalog"
    name_plural = "Catalogs"
    icon = "fa-solid fa-list"

    can_edit = False
    can_create = False
    can_delete = False
    can_export = False

    form_widget_args = {"name": {"readonly": True}, "is_active": {"readonly": True}, "categories": {"readonly": True}}

    column_list = ("id", "name", "page", "is_active")
    column_details_exclude_list = ("categories",)
    column_labels = {"id": "ID", "guid": "GUID", "name": "Name", "page": "Page", "is_active": "Is active"}
    column_default_sort = [("name", False)]

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
