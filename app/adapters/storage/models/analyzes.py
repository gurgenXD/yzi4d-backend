import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.adapters.storage.db.base_model import BaseModel

analyzes_types_analyzes_table = sa.Table(
    "analyzes_types_analyzes",
    BaseModel.metadata,
    sa.Column("analysis_type_id", sa.ForeignKey("analyzes_types.id"), primary_key=True),
    sa.Column("analysis_id", sa.ForeignKey("analyzes.id"), primary_key=True),
)


class AnalysisType(BaseModel):
    """Тип анализов."""

    __tablename__ = "analyzes_types"

    name: Mapped[str] = mapped_column(sa.String(30))
    description: Mapped[str | None] = mapped_column(sa.Text())

    analyzes: Mapped[set["Analysis"]] = relationship(
        "Analysis", secondary=analyzes_types_analyzes_table, back_populates="analyzes_types"
    )

    def __str__(self) -> str:
        return self.name


class Analysis(BaseModel):
    """Анализы."""

    __tablename__ = "analyzes"

    name: Mapped[str] = mapped_column(sa.String(length=30))
    preparation: Mapped[str | None] = mapped_column(sa.Text())
    period: Mapped[str] = mapped_column(sa.String(length=30))
    is_active: Mapped[bool] = mapped_column(default=False)

    analyzes_types: Mapped[set["AnalysisType"]] = relationship(
        "AnalysisType", secondary=analyzes_types_analyzes_table, back_populates="analyzes"
    )

    def __str__(self) -> str:
        return self.name
