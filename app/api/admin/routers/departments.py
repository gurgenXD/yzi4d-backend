from typing import Any

from sqladmin import ModelView
from wtforms.fields import BooleanField, FileField

from app.adapters.storage.models.departments import Department
from utils.admin.files import save_file


class DepartmentAdmin(ModelView, model=Department):
    """Отделения в админ панели."""

    name = "Отделение"
    name_plural = "Отделения"
    icon = "fa-solid fa-hospital"

    form_overrides = {"is_active": BooleanField, "photo": FileField}
    form_widget_args = {"is_active": {"class": "form-check-input"}, "photo": {"required": False}}

    column_list = ("id", "name", "is_active")
    column_labels = {
        "id": "ID",
        "name": "Отделение",
        "tags": "Тэги",
        "short_description": "Короткое описание",
        "description": "Описание",
        "photo": "Фото",
        "is_active": "Активно",
        "office": "Адрес",
    }

    form_ajax_refs = {"office": {"fields": ("address",), "order_by": "address"}}

    async def insert_model(self, data: dict[str, Any]) -> None:
        """Переопределение создания модели."""
        await save_file(("photo",), data, "departments")
        return await super().insert_model(data)

    async def update_model(self, pk: int, data: dict[str, Any]) -> None:
        """Переопределение обновления модели."""
        await save_file(("photo",), data, "departments")
        return await super().update_model(pk, data)
