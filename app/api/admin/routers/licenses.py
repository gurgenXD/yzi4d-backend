from typing import Any

from sqladmin import ModelView
from wtforms.fields import BooleanField, FileField

from app.adapters.storage.models.licenses import License
from utils.admin.files import save_file


class LicenseAdmin(ModelView, model=License):
    """Лицензии в админ панели."""

    name = "Лицензия"
    name_plural = "Лицензии"
    icon = "fa-solid fa-file-contract"

    form_overrides = {"is_active": BooleanField, "document": FileField}
    form_widget_args = {"is_active": {"class": "form-check-input"}, "document": {"required": False}}

    column_list = ("id", "title", "is_active")
    column_labels = {
        "id": "ID",
        "title": "Название лицензии",
        "document": "Документ",
        "is_active": "Актуально",
    }

    async def insert_model(self, data: dict[str, Any]) -> None:
        """Переопределение создания модели."""
        await save_file(("document",), data, "licenses")
        return await super().insert_model(data)

    async def update_model(self, pk: int, data: dict[str, Any]) -> None:
        """Переопределение обновления модели."""
        await save_file(("document",), data, "licenses")
        return await super().update_model(pk, data)
