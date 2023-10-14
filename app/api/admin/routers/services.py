from sqladmin import ModelView

from app.adapters.storage.models.services import Service, Category, Catalog


class ServiceAdmin(ModelView, model=Service):
    """Услуги в админ панели."""

    name = "Service"
    name_plural = "Services"
    category = "Services"
    icon = "fa-solid fa-syringe"
    page_size = 20
    page_size_options = [20, 50, 100]

    can_edit = False
    can_create = False
    can_delete = False
    can_export = False

    column_list = ("id", "name", "is_active")
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
    column_searchable_list = ["name", "guid"]


class ServiceCategoryAdmin(ModelView, model=Category):
    """Категории услуг в админ панели."""

    name = "Category"
    name_plural = "Categories"
    category = "Services"
    icon = "fa-solid fa-folder-tree"

    can_edit = False
    can_create = False
    can_delete = False
    can_export = False

    column_list = ("id", "name", "parent", "catalog", "is_active")
    column_details_exclude_list = ("parent_id", "catalog_id")
    column_labels = {
        "id": "ID",
        "guid": "GUID",
        "icon": "Icon",
        "name": "Name",
        "is_active": "Is active",
        "children": "Children",
        "parent": "Parent",
        "catalog": "Catalog",
        "services": "Services",
    }
    column_default_sort = [("name", False)]


class ServiceCatalogAdmin(ModelView, model=Catalog):
    """Каталоги услуг в админ панели."""

    name = "Catalog"
    name_plural = "Catalogs"
    category = "Services"
    icon = "fa-solid fa-list"

    can_create = False
    can_delete = False
    can_export = False

    form_widget_args = {"name": {"readonly": True}, "is_active": {"readonly": True}, "categories": {"readonly": True}}

    column_list = ("id", "name", "page", "is_active")
    column_labels = {
        "id": "ID",
        "guid": "GUID",
        "name": "Name",
        "page": "Page",
        "is_active": "Is active",
        "categories": "Categories",
    }
    column_default_sort = [("name", False)]
