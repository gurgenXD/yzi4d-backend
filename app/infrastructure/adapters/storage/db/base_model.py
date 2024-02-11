from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    """Базовый класс моделей."""

    type_annotation_map = {datetime: sa.TIMESTAMP(timezone=True)}
