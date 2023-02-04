from pydantic import BaseModel


class ServiceSchema(BaseModel):
    """Схема услуги."""

    name: str
    on_main: bool
    is_active: bool

    class Config:
        orm_mode = True
