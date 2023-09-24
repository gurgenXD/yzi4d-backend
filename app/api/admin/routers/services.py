from sqladmin import ModelView

from app.adapters.storage.models.services import Service


class ServiceAdmin(ModelView, model=Service):
    """Услуги в админ панели."""

    name = "Услуга"
    name_plural = "Услуги"
    icon = "fa-solid fa-syringe"
    can_create = False
    can_delete = False

    form_include_pk = True
    form_widget_args = {
        "id": {"readonly": True},
        "parent_id": {"readonly": True},
        "name": {"readonly": True},
        "parent": {"readonly": True},
        "patronymic": {"readonly": True},
    }

    column_list = ("name", "id", "parent_id", "is_active", "on_main")
    column_labels = {
        "id": "ID",
        "name": "Услуга",
        "short_description": "Короткое описание услуги",
        "description": "Описание услуги",
        "is_active": "Активно",
        "on_main": "Вывод на главной",
        "parent": "Родитель",
        "parent_id": "ID родителя",
        "is_group": "Группа услуг",
    }
    column_default_sort = [("name", False)]
