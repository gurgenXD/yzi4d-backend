from datetime import datetime

from pydantic import BaseModel, Field


class SourceSpecialistSchema(BaseModel):
    """Схема специалистов из источника."""

    guid: str = Field(alias="Guid1C")
    name: str = Field(alias="Name")
    surname: str = Field(alias="Surname")
    patronymic: str | None = Field(alias="MiddleName")
    can_adult: bool = Field(alias="ReceptionAdult")
    can_child: bool = Field(alias="ReceptionChild")
    can_online: bool = Field(alias="ReceptionOnline")
    on_main: bool = Field(alias="ShowOnMain")
    start_work_date: datetime = Field(alias="GetStartedDate")
    description: str = Field(alias="Description")
    short_description: str = Field(alias="ShortDescription")
    is_hidden: bool = Field(alias="Hide")
