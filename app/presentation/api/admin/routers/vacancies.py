from fastapi import Request
from sqladmin import ModelView

from app.infrastructure.adapters.storage.models.vacancies import Vacancy, VacancyCategory
from app.presentation.api.admin.permissions import PermissionType


class VacancyAdmin(ModelView, model=Vacancy):
    """Вакансии в админ панели."""

    name = "Vacancy"
    name_plural = "Vacancies"
    icon = "fa-solid fa-file-contract"

    can_export = False

    column_list = ("id", "name", "is_active")
    column_details_exclude_list = ("category_id",)
    column_labels = {"id": "ID", "name": "Name", "is_active": "Is active", "category": "Category"}

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


class VacancyCategoryAdmin(ModelView, model=VacancyCategory):
    """Категории вакансий в админ панели."""

    name = "Vacancy Category"
    name_plural = "Vacancies Categories"
    icon = "fa-solid fa-folder-tree"

    can_export = False

    column_list = ("id", "name", "position", "is_active")
    column_details_exclude_list = ("vacancies",)
    column_labels = {"id": "ID", "name": "Name", "position": "Position", "is_active": "Is active"}

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
