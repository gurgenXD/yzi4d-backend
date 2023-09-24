from datetime import date

from pydantic import BaseModel, Field


class SourceSpecialistSchema(BaseModel):
    """Схема специалистов из источника."""

    id: str = Field(alias="Guid1C")
    name: str = Field(alias="Name")
    surname: str = Field(alias="Surname")
    patronymic: str | None = Field(alias="MiddleName")
    can_adult: bool = Field(alias="ReceptionAdult")
    can_child: bool = Field(alias="ReceptionChild")

    education: str = "education"
    start_work_date: date = Field(default_factory=date.today)
    on_main: bool = False
    is_active: bool = True
    can_online: bool = False
