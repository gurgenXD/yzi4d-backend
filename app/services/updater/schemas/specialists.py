from pydantic import BaseModel, Field


class SourceSpecialistSchema(BaseModel):
    """Схема специалистов из источника."""

    guid_1c: str = Field(alias="Guid1C")
    name: str = Field(alias="Name")
    surname: str = Field(alias="Surname")
    patronymic: str | None = Field(alias="MiddleName")
