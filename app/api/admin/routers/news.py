from sqladmin import ModelView

from app.adapters.storage.models.news import News


class NewsAdmin(ModelView, model=News):
    """Новости в админ панели."""

    name = "News"
    name_plural = "News"
    icon = "fa-solid fa-newspaper"

    column_list = ("id", "title", "preview", "created")
    column_labels = {
        "id": "ID",
        "title": "Title",
        "preview": "Preview",
        "description": "Description",
        "created": "Created",
        "photo": "Photo",
        "is_active": "Is active",
    }
