from pydantic import BaseModel


class VacancyEntity(BaseModel):
    """Сущность вакансии."""

    name: str
    is_active: bool

    class Config:
        from_attributes = True


class VacancyCategoryEntity(BaseModel):
    """Сущность категории вакансий."""

    name: str
    position: int
    is_active: bool
    vacancies: list[VacancyEntity] = []

    class Config:
        from_attributes = True
