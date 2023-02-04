from sqladmin import ModelView
from wtforms.fields import BooleanField

from app.adapters.storage.models.pages import Page


class PagesAdmin(ModelView, model=Page):
    """Статичные страницы в админ панели."""

    name = "Статичная страница"
    name_plural = "Статичные страницы"
    icon = "fa-solid fa-file"

    form_overrides = {"is_active": BooleanField}
    form_widget_args = {"is_active": {"class": "form-check-input"}}

    column_list = ("id", "title", "slug", "is_active")
    column_labels = {
        "id": "ID",
        "slug": "Slug",
        "title": "Заголовок",
        "body": "Тело",
        "is_active": "Актуально",
    }
