from datetime import datetime

from pydantic import BaseModel


class PromotionSchema(BaseModel):
    """Схема акции."""

    sale: str
    title: str
    description: str
    photo: str | None
    services: str
    date_start: datetime
    date_end: datetime
    url: str
    is_active: bool
    on_main: bool

    class Config:
        orm_mode = True
