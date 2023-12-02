from zoneinfo import ZoneInfo

import wtforms
from sqladmin import ModelView
from sqlalchemy import Column

from app.adapters.storage.models.consultations import Consultation
from app.services.types.consultations import ConsultationStatus


def format_status(value: Consultation, _field: Column) -> str:
    """Форматирование статуса."""
    return ConsultationStatus(value.status).show_val


def format_created(value: Consultation, _field: Column) -> str:
    """Форматирование даты."""
    return value.created.astimezone(tz=ZoneInfo("Europe/Moscow")).strftime("%d.%m.%Y %H:%M")


class ConsultationAdmin(ModelView, model=Consultation):
    """Онлайн-консультация в админ панели."""

    name = "Online consultation"
    name_plural = "Online consultations"
    icon = "fa-solid fa-phone-volume"

    can_export = False
    can_delete = False
    can_create = False

    form_args = {"status": {"choices": ConsultationStatus.choices()}}
    form_excluded_columns = ("created",)
    form_overrides = {"status": wtforms.SelectField}

    column_formatters = {"status": format_status, "created": format_created}
    column_formatters_detail = {"status": format_status, "created": format_created}
    column_list = ("id", "name", "phone", "specialist", "status", "created")
    column_default_sort = [("created", True)]
    column_sortable_list = ("status", "name", "id", "created")
    column_searchable_list = ("name", "id", "status", "phone", "specialist")
    column_labels = {
        "id": "ID",
        "name": "Name",
        "phone": "Phone",
        "specialist": "Specialist",
        "created": "Created",
        "status": "Status",
        "comments": "Commments",
    }
