from datetime import datetime

from pydantic import BaseModel


class NewsSchema(BaseModel):
    """Схема контакта."""

    title: str
    preview: str
    created: datetime
    description: str
    photo: str | None
    is_active: bool

    class Config:
        orm_mode = True
