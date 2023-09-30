import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.adapters.storage.db.base_model import BaseModel
from fastapi_storages.integrations.sqlalchemy import FileType


from fastapi_storages import FileSystemStorage
from utils.constants import MEDIA_DIR


class DocumentCategory(BaseModel):
    """Категория документов."""

    __tablename__ = "documents_categories"

    id: Mapped[int] = mapped_column(sa.BigInteger(), primary_key=True, autoincrement=True)
    position: Mapped[int]
    is_active: Mapped[bool]

    documents: Mapped["Document"] = relationship("Document", back_populates="category")


class Document(BaseModel):
    """Документ."""

    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(sa.BigInteger(), primary_key=True, autoincrement=True)
    guid: Mapped[str] = mapped_column(sa.String(36), unique=True)
    name: Mapped[str] = mapped_column(sa.String(50))
    file: Mapped[str] = mapped_column(FileType(storage=FileSystemStorage(path=str(MEDIA_DIR / "documents"))))
    link: Mapped[str | None] = mapped_column(sa.String(255))
    is_active: Mapped[bool]

    category_id: Mapped[str | None] = mapped_column(
        sa.BigInteger(), sa.ForeignKey("documents_categories.id", ondelete="SET NULL")
    )

    category: Mapped["DocumentCategory"] = relationship("DocumentCategory", back_populates="documents")
