from datetime import datetime

from pydantic import BaseModel, Field


class SourceSpecialistSchema(BaseModel):
    """Схема специалистов из источника."""

    guid: str = Field(validation_alias="Guid1C")
    name: str = Field(validation_alias="Name")
    surname: str = Field(validation_alias="Surname")
    patronymic: str | None = Field(validation_alias="MiddleName")
    can_adult: bool = Field(validation_alias="ReceptionAdult")
    can_child: bool = Field(validation_alias="ReceptionChild")
    can_online: bool = Field(validation_alias="ReceptionOnline")
    on_main: bool = Field(validation_alias="ShowOnMain")
    start_work_date: datetime = Field(validation_alias="GetStartedDate")
    description: str = Field(validation_alias="Description")
    short_description: str = Field(validation_alias="ShortDescription")
    is_hidden: bool = Field(validation_alias="Hide")
