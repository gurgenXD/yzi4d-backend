from enum import Enum


class UpdaterStatusType(Enum):
    """Статусы обновления."""

    PROCESSING = "processing"
    SUCCESS = "success"
    FAILURE = "failure"
