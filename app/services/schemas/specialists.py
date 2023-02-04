from datetime import date

from pydantic import BaseModel


class SpecializationSchema(BaseModel):
    """Схема специализации."""

    name: str

    class Config:
        orm_mode = True


class SpecialistSchema(BaseModel):
    """Схема специалиста."""

    name: str
    surname: str
    patronymic: str | None
    photo: str | None
    start_work_date: date
    description: str
    titles: str | None
    specializations: list[SpecializationSchema]

    class Config:
        orm_mode = True
