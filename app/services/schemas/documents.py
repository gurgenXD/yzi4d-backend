from pydantic import BaseModel


class DocumentSchema(BaseModel):
    """Схема документа."""

    title: str
    photo: str | None
    is_active: bool

    class Config:
        from_attributes = True
