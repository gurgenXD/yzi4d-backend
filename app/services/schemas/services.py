from pydantic import BaseModel


class ServiceSchema(BaseModel):
    """Схема услуги."""

    id: str
    service_type_id: int
    name: str
    short_description: str | None
    description: str | None
    on_main: bool
    is_active: bool

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
