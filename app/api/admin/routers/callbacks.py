from sqladmin import ModelView
from wtforms.fields import BooleanField

from app.adapters.storage.models.callbacks import Callback


class CallbacksAdmin(ModelView, model=Callback):
    """Обратные звонки в админ панели."""

    name = "Обратный звонок"
    name_plural = "Обратные звонки"
    icon = "fa-solid fa-phone"

    form_overrides = {"answered": BooleanField}
    form_widget_args = {"answered": {"class": "form-check-input"}}

    column_list = ("id", "name", "phone", "answered")
    column_labels = {
        "id": "ID",
        "name": "Имя",
        "phone": "Телефон",
        "message": "Сообщение",
        "created": "Актуально",
        "answered": "Звонили",
        "call_back_time": "Время обратного звонка",
    }
