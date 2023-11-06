from sqladmin import ModelView

from app.adapters.storage.models.documents import Document, DocumentCategory


class DocumentAdmin(ModelView, model=Document):
    """Документы в админ панели."""

    name = "Document"
    name_plural = "Documents"
    icon = "fa-solid fa-file-contract"
    category = "Documents"

    can_export = False

    column_list = ("id", "name", "link", "is_active")
    column_details_exclude_list = ("category_id",)
    column_labels = {"id": "ID", "name": "Name", "link": "Link", "is_active": "Is active", "category": "Category"}


class DocumentCategoryAdmin(ModelView, model=DocumentCategory):
    """Категории документы в админ панели."""

    name = "Category"
    name_plural = "Categories"
    icon = "fa-solid fa-folder-tree"
    category = "Documents"

    can_export = False

    column_list = ("id", "name", "position", "is_active")
    column_labels = {"id": "ID", "name": "Name", "position": "Position", "is_active": "Is active"}
