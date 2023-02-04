from sqladmin import ModelView
from wtforms.fields import BooleanField

from app.adapters.storage.models.services import Service, ServiceType


class ServiceTypeAdmin(ModelView, model=ServiceType):
    """Категории услуг в админ панели."""

    name = "Категория услуг"
    name_plural = "Категории услуг"
    icon = "fa-solid fa-tablets"

    form_overrides = {"on_main": BooleanField}
    form_widget_args = {"on_main": {"class": "form-check-input"}}

    column_list = ("id", "name")
    column_labels = {
        "id": "ID",
        "name": "Категория услуг",
        "on_main": "Выводить на гланой",
        "services": "Услуги",
    }

    form_ajax_refs = {"services": {"fields": ("name",), "order_by": "name"}}


class ServiceAdmin(ModelView, model=Service):
    """Услуги в админ панели."""

    name = "Услуга"
    name_plural = "Услуги"
    icon = "fa-solid fa-syringe"

    form_overrides = {"is_active": BooleanField, "on_main": BooleanField}
    form_widget_args = {
        "is_active": {"class": "form-check-input"},
        "on_main": {"class": "form-check-input"},
    }

    column_list = ("id", "name", "is_active", "on_main")
    column_labels = {
        "id": "ID",
        "name": "Услуги",
        "is_active": "Активно",
        "on_main": "Вывод на главной",
        "service_type": "Категория услуг",
    }
    column_details_exclude_list = ("service_type_id",)

    form_ajax_refs = {"service_type": {"fields": ("name",), "order_by": "name"}}
