from pydantic import BaseModel, Field, field_validator


EMPTY_GUID = "00000000-0000-0000-0000-000000000000"


class ServicePriceSchema(BaseModel):
    """Схема цены услуги."""

    office_id: str = Field(alias="DivisionGuid1C")
    specialist_id: str = Field(alias="SpecGuid1C")
    price: int = Field(alias="Price")
    is_active: bool = True

    @field_validator("price", mode="before")
    @classmethod
    def validate_price(cls, v) -> int:
        """Валидировать цену."""
        try:
            return int(v)
        except ValueError:
            return 0


class ServiceExtSchema(BaseModel):
    """Расширенная схема услуги."""

    id: str = Field(alias="Guid1C")
    name: str = Field(alias="ProductName")
    # ready_from: int | None = Field(alias="ReadyFrom")
    # ready_to: int | None = Field(alias="ReadyTo")
    # description: str | None = Field(alias="Description")
    # preparation: str | None = Field(alias="Preparation")
    prices: list[ServicePriceSchema] = Field(alias="ProductPrice")
    is_active: bool = True


class ServiceSchema(BaseModel):
    """Схема услуги."""

    guid: str = Field(alias="Guid1C")


class CatalogItemSchema(BaseModel):
    """Схема элемента каталога."""

    id: str = Field(alias="Guid1C")
    name: str = Field(alias="CatalogName")
    parent_id: str | None = Field(alias="ParentGuid1C")
    services: list[ServiceSchema] = Field(alias="ProductList")
    is_active: bool = True

    @field_validator("parent_id", mode="before")
    @classmethod
    def empty_str_to_none(cls, v) -> str | None:
        """Перевести пустую строку в None."""
        return None if v == EMPTY_GUID else v


class CatalogSchema(BaseModel):
    """Схема каталога."""

    id: str = Field(alias="Guid1C")
    name: str = Field(alias="CatalogName")
    is_active: bool = True
