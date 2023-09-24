from pydantic import BaseModel


class PageSchema(BaseModel):
    """Схема статичной страницы."""

    slug: str
    title: str
    body: str
    is_active: bool

    class Config:
        from_attributes = True
