from datetime import date

from pydantic import BaseModel


class PromotionEntity(BaseModel):
    """Сущность акции."""

    name: str
    sale: str
    sale_period: str
    description: str | None
    photo: str
    date_start: date
    date_end: date
    on_main: bool

    class Config:
        from_attributes = True
