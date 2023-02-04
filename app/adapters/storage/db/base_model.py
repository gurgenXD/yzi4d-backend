from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseModel(DeclarativeBase):
    """Базовый класс моделей."""

    type_annotation_map = {datetime: sa.TIMESTAMP(timezone=True)}

    id: Mapped[int] = mapped_column(sa.BigInteger(), primary_key=True, autoincrement=True)
