from datetime import datetime, timedelta

from markupsafe import Markup
from sqladmin import ModelView
from sqlalchemy import Column

from app.adapters.storage.models import Update
from app.services.updater.types import UpdaterStatusType
from utils.admin.formats import datetime_format, timedelta_format


def format_status(value: str, _field: Column) -> Markup:
    """Отформатировать статус."""
    mapping = {
        UpdaterStatusType.SUCCESS.value: '<i class="fa fa-check text-success"></i>',
        UpdaterStatusType.FAILURE.value: '<i class="fa fa-times text-danger"></i>',
        UpdaterStatusType.PROCESSING.value: '<i class="fa-solid fa-spinner"></i>',
    }
    return Markup(mapping[str(value)])


class UpdatesAdmin(ModelView, model=Update):
    """Сведения об обновлениях."""

    name = "Update"
    name_plural = "Updates"
    icon = "fa-solid fa-arrows-rotate"

    can_edit = False
    can_create = False
    can_delete = False
    can_export = False

    update_button = True

    column_formatters = {"status": format_status}
    column_formatters_detail = {"status": format_status}

    column_list = ("id", "start_update", "end_update", "duration", "data_type", "status")
    column_labels = {
        "id": "ID",
        "status": "Status",
        "start_update": "Start",
        "end_update": "End",
        "duration": "Duration",
        "error_log": "Errors",
        "data_type": "Data type",
    }
    column_default_sort = [("start_update", True)]
    column_type_formatters = {
        **ModelView.column_type_formatters,
        datetime: datetime_format,
        timedelta: timedelta_format,
    }
