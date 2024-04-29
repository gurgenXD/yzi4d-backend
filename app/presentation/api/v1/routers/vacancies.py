from fastapi import APIRouter

from app.container import CONTAINER
from app.domain.entities.vacancies import VacancyCategoryEntity


TAG = "vacancies"
PREFIX = f"/{TAG}"


router = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("")
async def get_vacancies() -> list[VacancyCategoryEntity]:
    """Получить вакансии."""
    adapter = CONTAINER.vacancies_adapter()
    return await adapter.get_all()
