from pydantic import BaseModel


class AnalysisEntity(BaseModel):
    """Сущность анализа."""

    name: str
    preparation: str | None
    period: str
    is_active: bool

    class Config:
        from_attributes = True


class AnalysisTypeEntity(BaseModel):
    """Сущность категории анализа."""

    name: str
    description: str | None

    class Config:
        from_attributes = True


class AnalysisTypeWithAnalyzesEntity(BaseModel):
    """Сущность связи категории анализов с анализом."""

    name: str
    description: str | None
    analyzes: list[AnalysisEntity]

    class Config:
        from_attributes = True
