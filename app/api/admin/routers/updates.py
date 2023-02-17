from sqladmin import ModelView

from app.adapters.storage.models.updates import Update


class UpdatesAdmin(ModelView, model=Update):
    """Сведения об обновлениях."""

    name = "Обновление"
    name_plural = "Обновления"
    icon = "fa-solid fa-arrows-rotate"
    can_edit = False
    can_create = False
    can_delete = False
    update_button = True
    list_template = "sqladmin/list.html"

    column_list = ("status", "start_update", "end_update", "error_log")
    column_labels = {
        "status": "Статус обновления",
        "start_update": "Начало обновления",
        "end_update": "Конец обновления",
        "error_log": "Ошибки",
    }
