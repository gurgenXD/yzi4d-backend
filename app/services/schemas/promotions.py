from datetime import date

from pydantic import BaseModel


class PromotionSchema(BaseModel):
    """Схема акции."""

    name: str
    sale: str
    description: str
    photo: str
    date_start: date
    date_end: date
    is_active: bool
    on_main: bool

    class Config:
        orm_mode = True
