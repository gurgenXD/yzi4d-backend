from fastapi import Request
from sqladmin import ModelView

from app.infrastructure.adapters.storage.models.callbacks import Callback
from app.presentation.api.admin.permissions import PermissionType


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

    def is_accessible(self, request: Request) -> bool:
        """Права на изменение."""
        if (permissions := request.session.get("permissions")) and PermissionType.ADMIN.value in permissions:
            return True
        return False

    def is_visible(self, request: Request) -> bool:
        """Права на просмотр."""
        if (permissions := request.session.get("permissions")) and PermissionType.ADMIN.value in permissions:
            return True
        return False
