import math
from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.sql import func

from app.infrastructure.adapters.storage.pagination.schemas import PaginationSchema


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.sql import Select


async def get_query_with_meta(
    session: "AsyncSession", query: "Select", page: int, page_size: int,
) -> tuple["Select", "PaginationSchema"]:
    """Получить запрос и мета по пагинации."""
    count_query = select(func.count()).select_from(query.subquery())
    items_count = (await session.execute(count_query)).scalar_one()

    pages_count = math.ceil(items_count / page_size) if items_count else 1
    page = 1 if page < 1 else pages_count if page > pages_count else page

    offset = page_size * (page - 1)
    paginated_query = query.limit(page_size).offset(offset)

    pagination_schema = PaginationSchema(
        total_pages=pages_count,
        items_count=items_count,
        current_page=page,
        page_size=page_size,
        has_prev=(page - 1 > 0),
        has_next=(page + 1 <= pages_count),
    )

    return paginated_query, pagination_schema
