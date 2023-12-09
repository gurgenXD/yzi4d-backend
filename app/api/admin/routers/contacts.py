from fastapi import Request
from sqladmin import ModelView

from app.adapters.storage.models.contacts import City, Department, Office
from app.api.admin.permissions import PermissionType


class OfficeAdmin(ModelView, model=Office):
    """Филиалы в админ панели."""

    name = "Office"
    name_plural = "Offices"
    icon = "fa-solid fa-hospital"

    can_export = False

    column_list = ("id", "city", "address", "is_active")
    column_details_exclude_list = ("city_id", "departments")

    column_labels = {
        "id": "ID",
        "address": "Address",
        "description": "Description",
        "work_time": "Work time",
        "phone": "Phone",
        "email": "E-mail",
        "main_doctor": "Main doctor",
        "main_doctor_work_time": "Main doctor work time",
        "point_x": "Point X",
        "point_y": "Point Y",
        "is_active": "Is active",
        "city": "City",
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


class CityAdmin(ModelView, model=City):
    """Города в админ панели."""

    name = "City"
    name_plural = "Cities"
    icon = "fa-solid fa-city"

    can_export = False

    column_list = ("id", "name", "is_active")
    column_details_exclude_list = ("offices",)
    column_labels = {"id": "ID", "name": "Name", "is_active": "Is active"}

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


class DepartmentAdmin(ModelView, model=Department):
    """Отделения в админ панели."""

    name = "Department"
    name_plural = "Departments"
    icon = "fa-solid fa-building"

    can_export = False

    column_list = ("id", "name", "office", "is_active")
    column_details_exclude_list = ("office_id",)
    column_labels = {
        "id": "ID",
        "name": "Name",
        "tags": "Tags",
        "short_description": "Short Description",
        "description": "Description",
        "photo": "Photo",
        "is_active": "Is active",
        "office": "Office",
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
