from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field


class CallbackEntity(BaseModel):
    """Сущность обратного звонка."""

    phone: str
    created: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))

    model_config = ConfigDict(validate_default=True, validate_assignment=True)
