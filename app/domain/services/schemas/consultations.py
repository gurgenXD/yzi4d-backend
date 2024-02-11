from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field

from app.domain.services.types.consultations import ConsultationStatus


class ConsultationSchema(BaseModel):
    """Схема онлайн-консультации."""

    name: str
    phone: str
    specialist: str
    created: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))
    status: str = ConsultationStatus.PENDING.val
    comments: str | None = None

    model_config = ConfigDict(validate_default=True, validate_assignment=True)
