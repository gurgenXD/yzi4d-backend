from enum import Enum
from dataclasses import dataclass


@dataclass
class StatusMixin:
    val: str
    show_val: str


class ConsultationStatus(StatusMixin, Enum):
    """Статусы онлайн-консультаций."""

    PENDING = "pending", "Новая"
    PROCCESSING = "proccesing", "В обработке"
    CANCELED = "canceled", "Отменена"
    WAITING = "waiting", "Ожидает"
    FINISHED = "finished", "Завершена"

    def __new__(cls, val: str, show_val: str):
        obj = object.__new__(cls)
        obj._value_ = val
        obj.show_val = show_val
        return obj

    @classmethod
    def choices(cls) -> list[tuple[str, str]]:
        return [(item.val, item.show_val) for item in cls]
