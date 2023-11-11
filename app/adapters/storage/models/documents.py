import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.adapters.storage.db.base_model import BaseModel


class DocumentCategory(BaseModel):
    """Категория документов."""

    __tablename__ = "documents_categories"

    id: Mapped[int] = mapped_column(sa.BigInteger(), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(sa.String(255))
    position: Mapped[int]
    is_active: Mapped[bool]

    documents: Mapped[list["Document"]] = relationship("Document", back_populates="category")

    def __str__(self) -> str:
        return self.name


class Document(BaseModel):
    """Документ."""

    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(sa.BigInteger(), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(sa.String(255))
    link: Mapped[str] = mapped_column(sa.String(255))
    is_active: Mapped[bool]

    category_id: Mapped[str | None] = mapped_column(
        sa.BigInteger(), sa.ForeignKey("documents_categories.id", ondelete="SET NULL")
    )

    category: Mapped["DocumentCategory"] = relationship("DocumentCategory", back_populates="documents")

    def __str__(self) -> str:
        return self.name
