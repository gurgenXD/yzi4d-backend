from sqladmin import ModelView
from utils.admin.formats import datetime_format
from app.adapters.storage.models.updates import Updater
from datetime import datetime


class UpdatesAdmin(ModelView, model=Updater):
    """Сведения об обновлениях."""

    name = "Обновление"
    name_plural = "Обновления"
    icon = "fa-solid fa-arrows-rotate"

    can_edit = False
    can_create = False
    can_delete = False

    update_button = True
    list_template = "sqladmin/list.html"

    column_list = ("id", "start_update", "end_update", "status")
    column_labels = {
        "status": "Статус",
        "start_update": "Начало",
        "end_update": "Конец",
        "error_log": "Ошибки",
    }
    column_default_sort = [(Updater.start_update, True)]
    column_type_formatters = {**ModelView.column_type_formatters, datetime: datetime_format}
