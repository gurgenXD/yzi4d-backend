from sqladmin import ModelView
from wtforms.fields import BooleanField, FileField

from app.adapters.storage.models.specialists import Specialist, Specialization
from utils.admin.files import save_file


class SpecializationAdmin(ModelView, model=Specialization):
    """Специальности в админ панели."""

    name = "Специальность"
    name_plural = "Специальности"
    icon = "fa-solid fa-stethoscope"

    column_list = ("id", "name")
    column_labels = {"id": "ID", "name": "Специальность", "specialists": "Специалисты"}

    form_ajax_refs = {"specialists": {"fields": ("name",), "order_by": "name"}}


class SpecialistAdmin(ModelView, model=Specialist):
    """Специалисты в админ панели."""

    name = "Специалист"
    name_plural = "Специалисты"
    icon = "fa-solid fa-user-doctor"
    create_template = "sqladmin/create.html"
    edit_template = "sqladmin/edit.html"

    form_overrides = {"on_main": BooleanField, "photo": FileField, "is_active": BooleanField}
    form_widget_args = {
        "on_main": {"class": "form-check-input"},
        "is_active": {"class": "form-check-input"},
    }

    column_list = ("id", "surname", "name", "on_main", "is_active")
    column_labels = {
        "id": "ID",
        "surname": "Фамилия",
        "name": "Имя",
        "patronymic": "Отчество",
        "description": "Описание",
        "titles": "Титулы",
        "photo": "Фото",
        "on_main": "Вывод на главной",
        "is_active": "Актуален",
        "start_work_date": "Начало работы",
        "specializations": "Специальности",
    }

    form_ajax_refs = {"specializations": {"fields": ("name",), "order_by": "name"}}

    async def insert_model(self, data: dict) -> None:
        """Переопределение создания модели."""

        await save_file(("photo",), data)
        return await super().insert_model(data)

    async def update_model(self, pk, data) -> None:
        """Переопределение обновления модели."""

        await save_file(("photo",), data)
        return await super().update_model(pk, data)
