from sqladmin import ModelView
from wtforms.fields import BooleanField

from app.adapters.storage.models.users import User


class UsersAdmin(ModelView, model=User):
    """Пользователи в админ панели."""

    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"

    form_overrides = {"is_active": BooleanField}
    form_widget_args = {"is_active": {"class": "form-check-input"}}

    column_list = ("id", "username", "created")
    column_labels = {
        "id": "ID",
        "username": "Пользователь",
        "email": "E-mail",
        "password": "Пароль",
        "created": "Дата создания",
        "is_active": "Активен",
    }
