from pydantic import BaseModel


class ServiceSchema(BaseModel):
    """Схема услуги."""

    id: int
    name: str
    short_description: str | None
    price: int
    old_price: int | None = None

    class Config:
        from_attributes = True


class ServiceTypeSchema(BaseModel):
    """Схема категории услуг."""

    id: str
    name: str
    on_main: bool

    class Config:
        from_attributes = True


class ServiceWithTypeSchema(ServiceSchema):
    """Схема связи категории услуг с услугой."""

    service_type: ServiceTypeSchema

    class Config:
        from_attributes = True


class CategorySchema(BaseModel):
    """Схема категорий услуг."""

    id: int
    name: str

    class Config:
        from_attributes = True
