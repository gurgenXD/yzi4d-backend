from typing import Any

from sqladmin import ModelView
from wtforms.fields import BooleanField, FileField

from app.adapters.storage.models.promotions import Promotion

from utils.admin.files import save_file


class PromotionsAdmin(ModelView, model=Promotion):
    """Акции в админ панели."""

    name = "Акция"
    name_plural = "Акции"
    icon = "fa-solid fa-percent"
    create_template = "sqladmin/create.html"
    edit_template = "sqladmin/edit.html"

    form_overrides = {"is_active": BooleanField, "on_main": BooleanField, "photo": FileField}
    form_widget_args = {
        "is_active": {"class": "form-check-input"},
        "on_main": {"class": "form-check-input"},
    }

    column_list = ("id", "name", "is_active", "on_main")
    column_labels = {
        "id": "ID",
        "name": "Название акции",
        "sale": "Скидка",
        "description": "Описание",
        "date_start": "Дата начала акции",
        "date_end": "Дата окончания акции",
        "photo": "Фото",
        "is_active": "Актуально",
        "on_main": "Выводить на главной",
    }

    async def insert_model(self, data: dict[str, Any]) -> None:
        """Переопределение создания модели."""

        await save_file(("photo",), data, "promotions")
        return await super().insert_model(data)

    async def update_model(self, pk: int, data: dict[str, Any]) -> None:
        """Переопределение обновления модели."""

        await save_file(("photo",), data, "promotions")
        return await super().update_model(pk, data)
