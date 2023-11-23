from sqladmin import ModelView

from app.adapters.storage.models.callbacks import Callback


class CallbackAdmin(ModelView, model=Callback):
    """Обратные звонки в админ панели."""

    name = "Callback"
    name_plural = "Callbacks"
    icon = "fa-solid fa-phone"

    can_export = False

    column_list = ("id", "name", "phone", "answered")
    column_labels = {
        "id": "ID",
        "name": "Name",
        "phone": "Phone",
        "message": "Message",
        "created": "Created",
        "answered": "Answered",
        "call_back_time": "Call back time",
    }
