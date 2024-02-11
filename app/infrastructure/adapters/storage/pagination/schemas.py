from typing import Generic, TypeVar

from pydantic import BaseModel


DataT = TypeVar("DataT")


class PaginationSchema(BaseModel):
    """Информация о пагинации."""

    current_page: int
    page_size: int
    total_pages: int
    items_count: int
    has_prev: bool
    has_next: bool


class Paginated(BaseModel, Generic[DataT]):
    """Шаблонная схема для ответа с пагинацией."""

    data: list[DataT]
    paging: PaginationSchema
