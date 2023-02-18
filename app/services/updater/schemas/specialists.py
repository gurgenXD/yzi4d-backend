from pydantic import BaseModel, Field
from datetime import date


class SourceSpecialistSchema(BaseModel):
    """Схема специалистов из источника."""

    guid_1c: str = Field(alias="Guid1C")
    name: str = Field(alias="Name")
    surname: str = Field(alias="Surname")
    patronymic: str | None = Field(alias="MiddleName")

    education: str = "education"
    start_work_date: date = Field(default_factory=date.today)
    on_main: bool = False
    is_active: bool = True
    can_online: bool = False
