from pydantic import BaseModel


class ServiceSchema(BaseModel):
    """Схема услуги."""

    id: int
    name: str
    description: str | None
    on_main: bool
    is_active: bool

    class Config:
        orm_mode = True


class ServiceTypeSchema(BaseModel):
    """Схема категории услуг."""

    id: int
    name: str
    on_main: bool

    class Config:
        orm_mode = True


class ServiceTypeWithServicesSchema(BaseModel):
    """Схема категории услуг."""

    id: int
    name: str
    on_main: bool
    services: list[ServiceSchema]

    class Config:
        orm_mode = True
