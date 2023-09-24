from enum import Enum


class UpdaterStatusType(Enum):
    """Статусы обновления."""

    PROCESSING = "processing"
    SUCCESS = "success"
    FAILURE = "failure"


class UpdaterDataType(Enum):
    """Обновляемая таблица."""

    SERVICES = "services"
    SPECIALISTS = "specialists"
    IMAGES = "images"
    CATALOGS = "catalogs"
