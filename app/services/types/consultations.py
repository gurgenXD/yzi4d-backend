from dataclasses import dataclass
from enum import Enum


@dataclass
class StatusMixin:
    """Mixin для статусов онлайн-консультаций."""

    val: str
    show_val: str


class ConsultationStatus(StatusMixin, Enum):
    """Статусы онлайн-консультаций."""

    PENDING = "pending", "Новая"
    PROCESSING = "processing", "В обработке"
    CANCELED = "canceled", "Отменена"
    WAITING = "waiting", "Ожидает"
    FINISHED = "finished", "Завершена"

    def __new__(cls, val: str, show_val: str) -> "ConsultationStatus":
        """Переопределение new."""
        obj = object.__new__(cls)
        obj._value_ = val
        obj.show_val = show_val
        return obj

    @classmethod
    def choices(cls) -> list[tuple[str, str]]:
        """Список статусов."""
        return [(item.val, item.show_val) for item in cls]
