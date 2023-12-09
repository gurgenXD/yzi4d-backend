from fastapi import Request
from sqladmin import ModelView

from app.adapters.storage.models.promotions import Promotion
from app.api.admin.permissions import PermissionType


class PromotionsAdmin(ModelView, model=Promotion):
    """Акции в админ панели."""

    name = "Promotion"
    name_plural = "Promotions"
    icon = "fa-solid fa-percent"

    can_export = False

    column_list = ("id", "name", "on_main", "date_start", "date_end")
    column_sortable_list = ("id", "on_main", "date_start", "date_end")
    column_searchable_list = ("id", "name")
    column_labels = {
        "id": "ID",
        "name": "Name",
        "sale": "Sale",
        "sale_period": "Sale Period",
        "description": "Description",
        "date_start": "Date start",
        "date_end": "Date end",
        "photo": "Photo",
        "on_main": "On main",
    }

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
