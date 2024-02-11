from pydantic import BaseModel


class StrictServiceSchema(BaseModel):
    """Схема услуги."""

    id: int
    name: str
    short_description: str | None
    price: int

    class Config:
        from_attributes = True


class ServiceSchema(StrictServiceSchema):
    """Схема услуги."""

    category_id: int
    category_name: str
    old_price: int | None = None
    description: str | None
    preparation: str | None

    class Config:
        from_attributes = True


class CategorySchema(BaseModel):
    """Схема категорий услуг."""

    id: int
    name: str
    icon: str | None = None

    services: list[StrictServiceSchema] | None = None

    class Config:
        from_attributes = True
