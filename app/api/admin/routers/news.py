from typing import Any

from sqladmin import ModelView
from wtforms.fields import BooleanField, FileField

from app.adapters.storage.models.news import News
from utils.admin.files import save_file


class NewsAdmin(ModelView, model=News):
    """Новости в админ панели."""

    name = "Новость"
    name_plural = "Новости"
    icon = "fa-solid fa-newspaper"

    form_overrides = {"is_active": BooleanField, "photo": FileField}
    form_widget_args = {"is_active": {"class": "form-check-input"}, "document": {"required": False}}

    column_list = ("id", "title", "preview", "created")
    column_labels = {
        "id": "ID",
        "title": "Заголовок",
        "preview": "Предпросмотр",
        "description": "Описание",
        "created": "Дата создания",
        "photo": "Фото",
        "is_active": "Актуально",
    }

    async def insert_model(self, data: dict[str, Any]) -> None:
        """Переопределение создания модели."""
        await save_file(("photo",), data, "news")
        return await super().insert_model(data)

    async def update_model(self, pk: int, data: dict[str, Any]) -> None:
        """Переопределение обновления модели."""
        await save_file(("photo",), data, "news")
        return await super().update_model(pk, data)
