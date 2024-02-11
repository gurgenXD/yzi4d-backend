from pydantic import BaseModel


class AnalysisSchema(BaseModel):
    """Схема анализа."""

    name: str
    preparation: str | None
    period: str
    is_active: bool

    class Config:
        from_attributes = True


class AnalysisTypeSchema(BaseModel):
    """Схема категории анализа."""

    name: str
    description: str | None

    class Config:
        from_attributes = True


class AnalysisTypeWithAnalyzesSchema(BaseModel):
    """Схема связи категории анализов с анализом."""

    name: str
    description: str | None
    analyzes: list[AnalysisSchema]

    class Config:
        from_attributes = True
