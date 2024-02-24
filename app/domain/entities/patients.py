from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator


class MemberEntitiy(BaseModel):
    """Сущность члена семьи."""

    id: str = Field(validation_alias="FamilyMemberGUID")
    full_name: str = Field(validation_alias="FamilyMember")


class DicountEntitiy(BaseModel):
    """Сущность скидки."""

    next: int = Field(validation_alias="NextDiscount")
    current: int = Field(validation_alias="CurrentDiscount")
    next_spent: int = Field(validation_alias="NextSavingsTo")
    current_spent: int = Field(validation_alias="TotalSavings")

    @field_validator("next_spent", "current_spent", mode="before")
    @classmethod
    def float_to_int(cls, value: Any) -> int:
        """Отбросить дробную часть числа."""
        return int(str(value).split(".")[0])


class PatientEntity(BaseModel):
    """Сущность пациента."""

    id: str = Field(validation_alias="middleName")
    name: str
    surname: str
    patronymic: str | None = Field(validation_alias="middleName")
    birth_date: str = Field(validation_alias="dateBirth")
    age: str
    gender: str = Field(validation_alias="sex")
    phone: str
    members: list[MemberEntitiy] = Field(validation_alias="FamilyMember")
    discount: list[DicountEntitiy] = Field(validation_alias="DiscountData")

    class Config:
        from_attributes = True


class PatientVisitServiceEntity(BaseModel):
    """Сущность услуги визита пациента."""

    id: str = Field(validation_alias="ServiceGUID")
    name: str = Field(validation_alias="ServiceNAME")
    price: int = Field(validation_alias="SumService")

    class Config:
        from_attributes = True


class PatientPlannedVisitEntity(BaseModel):
    """Сущность визита пациента."""

    id: str = Field(validation_alias="PacientID")
    date_start: str = Field(validation_alias="DateTime")
    specialist: str = Field(validation_alias="SpecialistNAME")
    address: str = Field(validation_alias="BranchNAME")
    total_price: int = Field(validation_alias="Sum")
    services: list[PatientVisitServiceEntity] = Field(validation_alias="Services")

    @field_validator("date_start", mode="before")
    @classmethod
    def convert_datetime(cls, value: str) -> str:
        """Конвертировать дату в другой формат."""
        # 21 февраля, 9:00
        return datetime.strptime(value, "%d.%m.%Y %H:%M:%S").strftime("%d.%m.%Y %H:%M")

    class Config:
        from_attributes = True
