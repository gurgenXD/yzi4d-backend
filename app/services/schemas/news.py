from datetime import datetime

from pydantic import BaseModel


class NewsSchema(BaseModel):
    """Схема новости."""

    title: str
    preview: str
    created: datetime
    description: str
    photo: str | None
    is_active: bool

    class Config:
        from_attributes = True
