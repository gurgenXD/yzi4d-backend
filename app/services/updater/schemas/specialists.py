from datetime import datetime

from pydantic import BaseModel, Field, field_validator, computed_field


class SpecializationSchema(BaseModel):
    """Схема специальности."""

    guid: str = Field(alias="SpecGuid1C")
    name: str = Field(alias="SpecName")
    is_active: bool = Field(alias="IsActive")

    class Config:
        frozen = True


class EducationSchema(BaseModel):
    """Схема образования специалиста."""

    name: str = Field(alias="EduName")
    year: str = Field(alias="EduYear")


class TitleSchema(BaseModel):
    """Схема титула специалиста."""

    name: str = Field(alias="AcademicDegreeName")


class SourceSpecialistSchema(BaseModel):
    """Схема специалистов из источника."""

    guid: str = Field(alias="Guid1C")
    name: str = Field(alias="Name")
    surname: str = Field(alias="Surname")
    patronymic: str | None = Field(alias="MiddleName")
    can_adult: bool = Field(alias="ReceptionAdult")
    can_child: bool = Field(alias="ReceptionChild")
    can_online: bool = False
    on_main: bool = Field(alias="ShowOnMain")
    start_work_date: datetime = Field(alias="GetStartedDate")
    description: str = Field(alias="Description")
    short_description: str = Field(alias="ShortDescription")
    is_hidden: bool = Field(alias="Hide")

    education: list[EducationSchema] = Field(alias="EduList")
    titles: list[TitleSchema] = Field(alias="AcademicDegreeList")

    specializations: set[SpecializationSchema] = Field(alias="SpecList")

    @computed_field
    @property
    def is_active(self) -> bool:
        """Активность специалиста."""
        return not self.is_hidden


class SpecialistImageSchema(BaseModel):
    """Схема фотографии специалиста."""

    data: str | None = Field(alias="ImageFoto")

    @field_validator("data", mode="before")
    @classmethod
    def empty_str_to_none(cls, v) -> str | None:
        """Перевести пустую строку в None."""
        return None if v == "" else v
