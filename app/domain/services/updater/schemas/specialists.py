from datetime import datetime

from pydantic import BaseModel, Field, computed_field, field_validator


class SpecializationSchema(BaseModel):
    """Схема специальности."""

    guid: str = Field(validation_alias="SpecGuid1C")
    name: str = Field(validation_alias="SpecName")
    is_hidden: bool = Field(validation_alias="Hide")

    @computed_field
    @property
    def is_active(self) -> bool:
        """Активность специальности."""
        return not self.is_hidden

    class Config:
        frozen = True


class EducationSchema(BaseModel):
    """Схема образования специалиста."""

    name: str = Field(validation_alias="EduName")
    year: str = Field(validation_alias="EduYear")


class TitleSchema(BaseModel):
    """Схема титула специалиста."""

    name: str = Field(validation_alias="AcademicDegreeName")


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
    seo_description: str | None = Field("seo_desciption")
    is_hidden: bool = Field(validation_alias="Hide")

    education: list[EducationSchema] = Field(validation_alias="EduList")
    titles: list[TitleSchema] = Field(validation_alias="AcademicDegreeList")

    specializations: set[SpecializationSchema] = Field(validation_alias="SpecList")

    @computed_field
    @property
    def is_active(self) -> bool:
        """Активность специалиста."""
        return not self.is_hidden


class SpecialistImageSchema(BaseModel):
    """Схема фотографии специалиста."""

    data: str | None = Field(validation_alias="ImageFoto")

    @field_validator("data", mode="before")
    @classmethod
    def empty_str_to_none(cls, v: str) -> str | None:
        """Перевести пустую строку в None."""
        return None if v == "" else v
