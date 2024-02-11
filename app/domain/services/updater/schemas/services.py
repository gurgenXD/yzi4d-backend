from pydantic import BaseModel, Field, computed_field, field_validator


EMPTY_GUID = "00000000-0000-0000-0000-000000000000"


class ServicePriceSchema(BaseModel):
    """Схема цены услуги."""

    office_guid: str = Field(alias="DivisionGuid1C")
    specialist_guid: str = Field(alias="SpecGuid1C")
    price: int = Field(alias="Price")
    is_active: bool = True


class ServiceExtSchema(BaseModel):
    """Расширенная схема услуги."""

    guid: str = Field(alias="Guid1C")
    name: str = Field(alias="ProductName")
    ready_from: int | None = Field(alias="ReadyFrom")
    ready_to: int | None = Field(alias="ReadyTo")
    description: str | None = Field(alias="Description")
    short_description: str | None = Field(alias="ShortDescription")
    preparation: str | None = Field(alias="Preparation")
    prices: list[ServicePriceSchema] = Field(alias="ProductPrice")
    is_hidden: bool = Field(alias="Hide")

    @computed_field
    @property
    def is_active(self) -> bool:
        """Активность специалиста."""
        return not self.is_hidden


class ServiceSchema(BaseModel):
    """Схема услуги."""

    guid: str = Field(alias="Guid1C")

    class Config:
        frozen = True


class CatalogItemSchema(BaseModel):
    """Схема элемента каталога."""

    guid: str = Field(alias="Guid1C")
    name: str = Field(alias="CatalogName")
    parent_guid: str | None = Field(alias="ParentGuid1C")
    services: set[ServiceSchema] = Field(alias="ProductList")
    is_active: bool = True

    @field_validator("parent_guid", mode="before")
    @classmethod
    def empty_str_to_none(cls, v: str) -> str | None:
        """Перевести пустую строку в None."""
        return None if v == EMPTY_GUID else v


class CatalogSchema(BaseModel):
    """Схема каталога."""

    guid: str = Field(alias="Guid1C")
    name: str = Field(alias="CatalogName")
    is_active: bool = True
