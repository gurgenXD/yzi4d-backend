from pydantic import BaseModel


class DocumentSchema(BaseModel):
    """Схема документа."""

    name: str
    link: str
    is_active: bool

    class Config:
        from_attributes = True


class DocumentCategorySchema(BaseModel):
    """Схема категории документов."""

    name: str
    position: int
    is_active: bool
    documents: list[DocumentSchema] = []

    class Config:
        from_attributes = True
