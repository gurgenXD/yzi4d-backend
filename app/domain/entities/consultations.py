from dataclasses import dataclass
from datetime import UTC, datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


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


class ConsultationEntity(BaseModel):
    """Сущность онлайн-консультации."""

    name: str
    phone: str
    specialist: str
    created: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))
    status: str = ConsultationStatus.PENDING.val
    comments: str | None = None

    model_config = ConfigDict(validate_default=True, validate_assignment=True)
