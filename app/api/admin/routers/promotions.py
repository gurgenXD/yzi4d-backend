from sqladmin import ModelView
from wtforms.fields import BooleanField

from app.adapters.storage.models.promotions import Promotion


class PromotionsAdmin(ModelView, model=Promotion):
    """Акции в админ панели."""

    name = "Акция"
    name_plural = "Акции"
    icon = "fa-solid fa-percent"

    form_overrides = {"is_active": BooleanField, "on_main": BooleanField}
    form_widget_args = {
        "is_active": {"class": "form-check-input"},
        "on_main": {"class": "form-check-input"},
    }

    column_list = ("id", "title", "is_active", "on_main")
    column_labels = {
        "id": "ID",
        "sale": "Акция",
        "title": "Предпросмотр",
        "description": "Описание",
        "date_start": "Дата начала акции",
        "date_end": "Дата окончания акции",
        "services": "Акционные услуги",
        "photo": "Фото",
        "url": "Ссылка на акцию",
        "is_active": "Актуально",
        "on_main": "Выводить на главной",
    }
