from pydantic import BaseModel


class SpecializationEntity(BaseModel):
    """Сущность специализации."""

    id: int
    name: str

    class Config:
        from_attributes = True
