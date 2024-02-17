from pydantic import BaseModel


class DocumentEntity(BaseModel):
    """Сущность документа."""

    name: str
    link: str
    is_active: bool

    class Config:
        from_attributes = True


class DocumentCategoryEntity(BaseModel):
    """Сущность категории документов."""

    name: str
    position: int
    is_active: bool
    documents: list[DocumentEntity] = []

    class Config:
        from_attributes = True
