from datetime import datetime

from markupsafe import Markup
from sqladmin import ModelView
from sqlalchemy import Column

from app.adapters.storage.models.updates import Updater
from app.services.updater.types import UpdaterStatusType
from utils.admin.formats import datetime_format


def format_status(value: str, _field: Column) -> Markup:
    """Отформатировать статус."""
    mapping = {
        UpdaterStatusType.SUCCESS.value: '<i class="fa fa-check text-success"></i>',
        UpdaterStatusType.FAILURE.value: '<i class="fa fa-times text-danger"></i>',
        UpdaterStatusType.PROCESSING.value: '<i class="fa-solid fa-arrows-rotate"></i>',
    }
    return Markup(mapping[str(value)])


class UpdatesAdmin(ModelView, model=Updater):
    """Сведения об обновлениях."""

    name = "Обновление"
    name_plural = "Обновления"
    icon = "fa-solid fa-arrows-rotate"

    can_edit = False
    can_create = False
    can_delete = False

    update_button = True

    column_formatters = {"status": format_status}  # type: ignore

    column_list = ("id", "start_update", "end_update", "status")
    column_labels = {
        "id": "ID",
        "status": "Статус",
        "start_update": "Начало",
        "end_update": "Конец",
        "error_log": "Ошибки",
    }
    column_default_sort = [("start_update", True)]
    column_type_formatters = {**ModelView.column_type_formatters, datetime: datetime_format}
