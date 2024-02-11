from datetime import date

from pydantic import BaseModel, computed_field

from utils.template_filters.humanize import calculate_ages, humanize_age


class SpecializationSchema(BaseModel):
    """Схема специализации."""

    id: int
    name: str

    class Config:
        from_attributes = True


class SpecialistCertificateSchema(BaseModel):
    """Схема сертификатов специалиста."""

    name: str
    path: str

    class Config:
        from_attributes = True


class SpecialistEducationSchema(BaseModel):
    """Схема обучения специалиста."""

    name: str
    year: str

    class Config:
        from_attributes = True


class SpecialistTitleSchema(BaseModel):
    """Схема титула специалиста."""

    name: str

    class Config:
        from_attributes = True


class SpecialistSchema(BaseModel):
    """Схема специалиста."""

    id: int
    name: str
    surname: str
    patronymic: str | None
    photo: str | None
    start_work_date: date
    education: list[SpecialistEducationSchema]
    activity: str | None
    description: str | None
    short_description: str | None
    titles: list[SpecialistTitleSchema]
    can_adult: bool
    can_child: bool
    can_online: bool
    specializations: list[SpecializationSchema]
    certificates: list[SpecialistCertificateSchema] = []

    @property
    def full_name(self) -> str:
        """Полное имя."""
        patronymic = f" {self.patronymic}" if self.patronymic else ""
        return f"{self.surname} {self.name}" + patronymic

    @computed_field
    @property
    def experience(self) -> str:
        """Стаж."""
        return humanize_age(calculate_ages(self.start_work_date))

    class Config:
        from_attributes = True
