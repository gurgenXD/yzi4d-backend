from pydantic import BaseModel


class StrictServiceEntity(BaseModel):
    """Сущность услуги."""

    id: int
    name: str
    short_description: str | None
    price: int

    class Config:
        from_attributes = True


class ServiceEntity(StrictServiceEntity):
    """Сущность услуги."""

    category_id: int
    category_name: str
    old_price: int | None = None
    description: str | None
    seo_description: str | None
    preparation: str | None

    class Config:
        from_attributes = True


class CategoryEntity(BaseModel):
    """Сущность категорий услуг."""

    id: int
    name: str
    icon: str | None = None

    services: list[StrictServiceEntity] | None = None

    class Config:
        from_attributes = True
