from sqladmin import ModelView

from app.adapters.storage.models.promotions import Promotion


class PromotionsAdmin(ModelView, model=Promotion):
    """Акции в админ панели."""

    name = "Promotion"
    name_plural = "Promotions"
    icon = "fa-solid fa-percent"

    can_export = False

    column_list = ("id", "name", "on_main", "date_end")
    column_labels = {
        "id": "ID",
        "name": "Name",
        "sale": "Sale",
        "description": "Description",
        "date_start": "Date start",
        "date_end": "Date end",
        "photo": "Photo",
        "on_main": "On main",
    }
