from pydantic import BaseModel, Field, field_validator, ValidationInfo
from password_validator import PasswordValidator


class MemberEntity(BaseModel):
    """Сущность члена семьи."""

    id: str = Field(validation_alias="FamilyMemberGUID")
    full_name: str = Field(validation_alias="FamilyMember")


class DiscountEntity(BaseModel):
    """Сущность скидки."""

    next: int = Field(validation_alias="nextDiscountPercentage")
    current: int = Field(validation_alias="discountPercentage")
    next_spent: int = Field(validation_alias="nextSavingsFrom")
    current_spent: int = Field(validation_alias="totalSaving")

    @field_validator("next_spent", "current_spent", mode="before")
    @classmethod
    def float_to_int(cls, value: float) -> int:
        """Отбросить дробную часть числа."""
        return int(str(value).split(".")[0])


class PatientEntity(BaseModel):
    """Сущность пациента."""

    id: str = Field(validation_alias="PacientID")
    name: str
    surname: str
    patronymic: str | None = Field(validation_alias="middleName")
    birth_date: str = Field(validation_alias="dateBirth")
    age: str
    gender: str = Field(validation_alias="sex")
    phone: str
    members: list[MemberEntity] = Field(validation_alias="FamilyMember")
    discount: DiscountEntity | None = Field(validation_alias="DiscountData")

    @field_validator("discount", mode="before")
    @classmethod
    def discount_validate(cls, value: dict) -> DiscountEntity | None:
        """Валидация скидок."""
        if not value:
            return None

        return DiscountEntity(**value)

    class Config:
        from_attributes = True


class PatientVisitServiceEntity(BaseModel):
    """Сущность услуги визита пациента."""

    name: str = Field(validation_alias="ServiceNAME")
    price: int = Field(validation_alias="SumService")

    class Config:
        from_attributes = True


class PatientPlannedVisitEntity(BaseModel):
    """Сущность запланированного визита пациента."""

    date_start: str = Field(validation_alias="DateTime")
    specialist: str = Field(validation_alias="SpecialistNAME")
    address: str = Field(validation_alias="BranchAddress")
    total_price: int = Field(validation_alias="Sum")
    services: list[PatientVisitServiceEntity] = Field(validation_alias="Services")

    class Config:
        from_attributes = True


class PatientFinishedVisitEntity(BaseModel):
    """Сущность завершенного визита пациента."""

    date_receipt: str = Field(validation_alias="dateReceipt")
    service: str = Field(validation_alias="service")
    file_path: str = Field(validation_alias="storagePath")
    specialist: str = Field(validation_alias="specialist")
    service_type: str = Field(validation_alias="researchType")
    header: str

    class Config:
        from_attributes = True


class ChangePasswordEntity(BaseModel):
    """Сущность смены пароля."""

    current_password: str
    new_password: str

    @field_validator("new_password")
    @classmethod
    def validate_password(cls, value: str, info: ValidationInfo) -> str:
        """Валидация пароля."""
        schema = PasswordValidator().letters().digits().uppercase().lowercase().min(6)

        if not schema.validate(value):
            raise ValueError("Password is not strong.")

        if value == info.data["current_password"]:
            raise ValueError("Enter another new password.")

        return value


class GeneratePasswordEntity(BaseModel):
    """Сущность генерации пароля."""

    username: str
