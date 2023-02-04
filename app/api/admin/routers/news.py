from sqladmin import ModelView
from wtforms.fields import BooleanField

from app.adapters.storage.models.news import News


class NewsAdmin(ModelView, model=News):
    """Новости в админ панели."""

    name = "Новость"
    name_plural = "Новости"
    icon = "fa-solid fa-newspaper"

    form_overrides = {"is_active": BooleanField}
    form_widget_args = {"is_active": {"class": "form-check-input"}}

    column_list = ("id", "title", "created")
    column_labels = {
        "id": "ID",
        "title": "Заголовок",
        "preview": "Предпросмотр",
        "description": "Описание",
        "created": "Дата создания",
        "photo": "Фото",
        "is_active": "Актуально",
    }
