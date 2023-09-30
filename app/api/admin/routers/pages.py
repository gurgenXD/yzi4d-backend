from sqladmin import ModelView

from app.adapters.storage.models.pages import Page


class PagesAdmin(ModelView, model=Page):
    """Статичные страницы в админ панели."""

    name = "Page"
    name_plural = "Pages"
    icon = "fa-solid fa-images"

    can_export = False

    column_list = ("id", "title", "url", "is_active")
    column_labels = {"id": "ID", "url": "URL", "title": "Title", "content": "Content", "is_active": "Is active"}
