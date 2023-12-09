from fastapi import Request
from sqladmin import ModelView

from app.adapters.storage.models.specialists import Certificate, Specialist, Specialization
from app.api.admin.permissions import PermissionType


class SpecializationAdmin(ModelView, model=Specialization):
    """Специальности в админ панели."""

    name = "Specialization"
    name_plural = "Specializations"
    icon = "fa-solid fa-stethoscope"

    can_edit = False
    can_create = False
    can_delete = False
    can_export = False

    column_list = ("id", "name", "is_active")
    column_sortable_list = ("name", "id")
    column_details_exclude_list = ("specialists",)
    column_labels = {"id": "ID", "guid": "GUID", "name": "Name", "is_active": "Is active"}
    column_default_sort = [("name", False)]

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


class SpecialistCertificateAdmin(ModelView, model=Certificate):
    """Сертификаты специалистов в админ панели."""

    name = "Certificate"
    name_plural = "Certificates"
    icon = "fa-solid fa-file-medical"

    can_edit = False
    can_create = False
    can_delete = False
    can_export = False

    column_list = ("id", "name", "file")
    column_details_exclude_list = ("specialist_id",)
    column_labels = {"id": "ID", "guid": "GUID", "specialist": "Specialist", "name": "Name", "file": "File"}

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


class SpecialistAdmin(ModelView, model=Specialist):
    """Специалисты в админ панели."""

    name = "Specialist"
    name_plural = "Specialists"
    icon = "fa-solid fa-user-doctor"

    can_edit = False
    can_create = False
    can_delete = False
    can_export = False

    column_list = ("id", "surname", "name", "patronymic", "on_main", "is_active")
    column_sortable_list = ("surname", "id", "on_main", "is_active")
    column_default_sort = [("surname", False)]
    column_searchable_list = ("surname", "name", "patronymic", "id", "guid")
    column_labels = {
        "id": "ID",
        "guid": "GUID",
        "surname": "Surname",
        "name": "Name",
        "patronymic": "Patronymic",
        "description": "Description",
        "short_description": "Short description",
        "education": "Education",
        "activity": "Activity",
        "titles": "Titles",
        "photo": "Photo",
        "on_main": "On main",
        "is_active": "Is active",
        "can_adult": "Can adult",
        "can_child": "Can child",
        "can_online": "Can online",
        "start_work_date": "Start work date",
        "specializations": "Specializations",
        "certificates": "Certificates",
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
