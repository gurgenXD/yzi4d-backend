from datetime import date

from pydantic import BaseModel


class SpecializationSchema(BaseModel):
    """Схема специализации."""

    name: str

    class Config:
        orm_mode = True


class SpecialistCertificateSchema(BaseModel):
    """Схема сертификатов специалиста."""

    name: str
    path: str

    class Config:
        orm_mode = True


class SpecialistSchema(BaseModel):
    """Схема специалиста."""

    id: int
    name: str
    surname: str
    patronymic: str | None
    photo: str | None
    start_work_date: date
    education: str
    activity: str | None
    description: str
    titles: str | None
    can_online: bool
    specializations: list[SpecializationSchema]
    certificates: list[SpecialistCertificateSchema]

    @property
    def full_name(self) -> str:
        """Полное имя."""
        patronymic = f" {self.patronymic}" if self.patronymic else ""
        return f"{self.surname} {self.name}" + patronymic

    class Config:
        orm_mode = True
