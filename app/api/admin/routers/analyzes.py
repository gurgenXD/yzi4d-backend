from sqladmin import ModelView
from wtforms.fields import BooleanField

from app.adapters.storage.models.analyzes import Analysis, AnalysisType


class AnalysisTypeAdmin(ModelView, model=AnalysisType):
    """Типы анализов в админ панели."""

    name = "Тип анализа"
    name_plural = "Типы анализов"
    icon = "fa-solid fa-vials"
    can_create = False
    can_delete = False

    column_list = ("id", "name")
    column_labels = {
        "id": "ID",
        "name": "Название",
        "description": "Описание",
        "analyzes": "Анализы",
    }

    column_default_sort = [("name", False)]
    form_ajax_refs = {"analyzes": {"fields": ("name",), "order_by": "name"}}


class AnalysisAdmin(ModelView, model=Analysis):
    """Анализы в админ панели."""

    name = "Анализ"
    name_plural = "Анализы"
    icon = "fa-solid fa-vial"

    form_overrides = {"is_active": BooleanField}
    form_widget_args = {"is_active": {"class": "form-check-input"}}

    column_list = ("id", "name", "preparation", "period", "is_active")
    column_labels = {
        "id": "ID",
        "name": "Название",
        "preparation": "Подготовка",
        "period": "Время проведения",
        "is_active": "Активно",
        "analyzes_types": "Типы анализов",
    }

    column_default_sort = [("name", False)]
    form_ajax_refs = {"analyzes_types": {"fields": ("name",), "order_by": "name"}}
