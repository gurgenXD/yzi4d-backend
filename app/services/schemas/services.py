from pydantic import BaseModel


class ServiceSchema(BaseModel):
    """Схема услуги."""

    id: int
    name: str
    category_id: int
    category_name: str
    short_description: str | None
    price: int
    old_price: int | None = None

    class Config:
        from_attributes = True


class ServiceExtendedSchema(ServiceSchema):
    """Схема расширенной услуги."""

    description: str | None
    preparation: str | None

    class Config:
        from_attributes = True


class CategorySchema(BaseModel):
    """Схема категорий услуг."""

    id: int
    name: str

    class Config:
        from_attributes = True
