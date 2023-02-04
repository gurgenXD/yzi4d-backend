from pydantic import BaseModel


class AnalysisSchema(BaseModel):
    """Схема анализа."""

    name: str
    preparation: str | None
    period: str
    is_active: bool

    class Config:
        orm_mode = True
