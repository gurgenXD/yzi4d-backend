from enum import Enum


class UpdaterStatusType(Enum):
    """Статусы обновления."""

    PROCESSING = "processing"
    SUCCESS = "success"
    FAILURE = "failure"


class UpdaterDataType(Enum):
    """Обновляемая таблица."""

    MAIN = "main"
    IMAGES = "images"


class CatalogPageType(Enum):
    """Тип страницы каталогов."""

    SERVICES = "services"
    ANALYZES = "analyzes"
    MAIN = "main"
