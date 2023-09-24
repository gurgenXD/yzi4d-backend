from datetime import date

from pydantic import BaseModel


class SpecializationSchema(BaseModel):
    """Схема специализации."""

    id: str
    name: str

    class Config:
        from_attributes = True


class SpecialistCertificateSchema(BaseModel):
    """Схема сертификатов специалиста."""

    name: str
    path: str

    class Config:
        from_attributes = True


class SpecialistSchema(BaseModel):
    """Схема специалиста."""

    id: str
    name: str
    surname: str
    patronymic: str | None
    photo: str | None
    start_work_date: date
    education: str
    activity: str | None
    description: str | None
    titles: str | None
    can_adult: bool
    can_child: bool
    can_online: bool
    specializations: list[SpecializationSchema]
    certificates: list[SpecialistCertificateSchema]

    @property
    def full_name(self) -> str:
        """Полное имя."""
        patronymic = f" {self.patronymic}" if self.patronymic else ""
        return f"{self.surname} {self.name}" + patronymic

    class Config:
        from_attributes = True
