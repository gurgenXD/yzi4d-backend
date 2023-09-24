from pydantic import BaseModel


class LicenseSchema(BaseModel):
    """Схема лицензии."""

    title: str
    photo: str | None
    is_active: bool

    class Config:
        from_attributes = True
