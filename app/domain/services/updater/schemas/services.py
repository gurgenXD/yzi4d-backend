from pydantic import BaseModel, Field, computed_field, field_validator


EMPTY_GUID = "00000000-0000-0000-0000-000000000000"


class ServicePriceSchema(BaseModel):
    """Схема цены услуги."""

    office_guid: str = Field(validation_alias="DivisionGuid1C")
    specialist_guid: str = Field(validation_alias="SpecGuid1C")
    price: int = Field(validation_alias="Price")
    is_active: bool = True


class ServiceExtSchema(BaseModel):
    """Расширенная схема услуги."""

    guid: str = Field(validation_alias="Guid1C")
    name: str = Field(validation_alias="ProductName")
    ready_from: int | None = Field(validation_alias="ReadyFrom")
    ready_to: int | None = Field(validation_alias="ReadyTo")
    description: str | None = Field(validation_alias="Description")
    short_description: str | None = Field(validation_alias="ShortDescription")
    seo_description: str | None = Field("seo_desciption")
    preparation: str | None = Field(validation_alias="Preparation")
    prices: list[ServicePriceSchema] = Field(validation_alias="ProductPrice")
    is_hidden: bool = Field(validation_alias="Hide")

    @computed_field
    @property
    def is_active(self) -> bool:
        """Активность специалиста."""
        return not self.is_hidden


class ServiceSchema(BaseModel):
    """Схема услуги."""

    guid: str = Field(validation_alias="Guid1C")

    class Config:
        frozen = True


class CatalogItemSchema(BaseModel):
    """Схема элемента каталога."""

    guid: str = Field(validation_alias="Guid1C")
    name: str = Field(validation_alias="CatalogName")
    parent_guid: str | None = Field(validation_alias="ParentGuid1C")
    services: set[ServiceSchema] = Field(validation_alias="ProductList")
    is_active: bool = True

    @field_validator("parent_guid", mode="before")
    @classmethod
    def empty_str_to_none(cls, v: str) -> str | None:
        """Перевести пустую строку в None."""
        return None if v == EMPTY_GUID else v


class CatalogSchema(BaseModel):
    """Схема каталога."""

    guid: str = Field(validation_alias="Guid1C")
    name: str = Field(validation_alias="CatalogName")
    is_active: bool = True
