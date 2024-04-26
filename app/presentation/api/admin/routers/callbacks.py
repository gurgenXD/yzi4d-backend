from zoneinfo import ZoneInfo

from fastapi import Request
from sqladmin import ModelView
from sqlalchemy import Column

from app.infrastructure.adapters.storage.models.callbacks import Callback
from app.presentation.api.admin.permissions import PermissionType


def format_created(value: Callback, _field: Column) -> str:
    """Форматирование даты."""
    return value.created.astimezone(tz=ZoneInfo("Europe/Moscow")).strftime("%d.%m.%Y %H:%M")


class CallbackAdmin(ModelView, model=Callback):
    """Обратные звонки в админ панели."""

    name = "Callback"
    name_plural = "Callbacks"
    icon = "fa-solid fa-phone"

    can_export = False
    can_delete = False
    can_create = False

    column_formatters = {"created": format_created}
    column_formatters_detail = {"created": format_created}

    form_excluded_columns = ("phone", "created")
    column_list = ("id", "phone", "created", "answered")
    column_labels = {"id": "ID", "phone": "Phone", "created": "Created", "answered": "Answered"}

    def is_accessible(self, request: Request) -> bool:
        """Права на изменение."""
        if (permissions := request.session.get("permissions")) and PermissionType.OPERATOR.value in permissions:
            return False
        return True

    def is_visible(self, request: Request) -> bool:
        """Права на просмотр."""
        if (permissions := request.session.get("permissions")) and PermissionType.OPERATOR.value in permissions:
            return False
        return True
