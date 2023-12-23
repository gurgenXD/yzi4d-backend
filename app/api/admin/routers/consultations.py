from zoneinfo import ZoneInfo

import wtforms
from fastapi import Request
from sqladmin import ModelView
from sqlalchemy import Column
from markupsafe import Markup
from app.adapters.storage.models.consultations import Consultation
from app.services.types.consultations import ConsultationStatus


def format_status(value: Consultation, _field: Column) -> str:
    """Форматирование статуса."""
    mask = '<p style="background-color:{color};padding:5px;margin:0px">{value}</p>'

    mapping = {
        ConsultationStatus.PENDING.val: mask.format(value=ConsultationStatus.PENDING.show_val, color="#e8e6e6"),
        ConsultationStatus.PROCESSING.val: mask.format(value=ConsultationStatus.PROCESSING.show_val, color="#c3dffa"),
        ConsultationStatus.CANCELED.val: mask.format(value=ConsultationStatus.CANCELED.show_val, color="#fcc8c2"),
        ConsultationStatus.WAITING.val: mask.format(value=ConsultationStatus.WAITING.show_val, color="#f7f6b7"),
        ConsultationStatus.FINISHED.val: mask.format(value=ConsultationStatus.FINISHED.show_val, color="#b2ebab"),
    }

    return Markup(mapping.get(str(value.status)) or str(value.status))


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
        "comments": "Comments",
    }

    def is_accessible(self, _request: Request) -> bool:
        """Права на изменение."""
        return True

    def is_visible(self, _request: Request) -> bool:
        """Права на просмотр."""
        return True
