from sqladmin import ModelView

from app.adapters.storage.models.promotions import Promotion


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
