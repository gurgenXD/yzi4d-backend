from typing import TYPE_CHECKING

import sqlalchemy as sa
from fastapi_storages import FileSystemStorage
from fastapi_storages.integrations.sqlalchemy import FileType
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.adapters.storage.db.base_model import BaseModel
from utils.constants import MEDIA_DIR


if TYPE_CHECKING:
    from app.infrastructure.adapters.storage.models.specialists import SpecialistService


categories_services_table = sa.Table(
    "categories_services_rel",
    BaseModel.metadata,
    sa.Column("service_category_id", sa.ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True),
    sa.Column("service_id", sa.ForeignKey("services.id", ondelete="CASCADE"), primary_key=True),
)


class Service(BaseModel):
    """Услуги."""

    __tablename__ = "services"

    id: Mapped[int] = mapped_column(sa.BigInteger(), primary_key=True, autoincrement=True)
    guid: Mapped[str] = mapped_column(sa.String(36), unique=True)
    name: Mapped[str] = mapped_column(sa.String(255))
    short_description: Mapped[str | None] = mapped_column(sa.Text())
    description: Mapped[str | None] = mapped_column(sa.Text())
    seo_description: Mapped[str | None] = mapped_column(sa.Text())
    preparation: Mapped[str | None] = mapped_column(sa.Text())
    ready_from: Mapped[int | None]
    ready_to: Mapped[int | None]
    is_active: Mapped[bool]

    categories: Mapped[list["Category"]] = relationship(
        "Category", secondary=categories_services_table, back_populates="services"
    )
    specialists_services: Mapped[list["SpecialistService"]] = relationship(
        "SpecialistService", back_populates="service"
    )

    def __str__(self) -> str:
        return self.name


class Category(BaseModel):
    """Категория услуг."""

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(sa.BigInteger(), primary_key=True, autoincrement=True)
    guid: Mapped[str] = mapped_column(sa.String(36), unique=True)
    name: Mapped[str] = mapped_column(sa.String(255))
    icon: Mapped[str | None] = mapped_column(FileType(storage=FileSystemStorage(path=str(MEDIA_DIR / "categories"))))
    is_active: Mapped[bool]

    parent_id: Mapped[int | None] = mapped_column(sa.BigInteger(), sa.ForeignKey("categories.id", ondelete="SET NULL"))
    catalog_id: Mapped[int] = mapped_column(sa.BigInteger(), sa.ForeignKey("catalogs.id", ondelete="CASCADE"))

    children: Mapped[list["Category"]] = relationship("Category", back_populates="parent")
    parent: Mapped["Category"] = relationship("Category", back_populates="children", remote_side=[id])
    catalog: Mapped["Catalog"] = relationship("Catalog", back_populates="categories")
    services: Mapped[list["Service"]] = relationship(
        "Service", secondary=categories_services_table, back_populates="categories"
    )

    def __str__(self) -> str:
        return self.name


class Catalog(BaseModel):
    """Каталог услуг."""

    __tablename__ = "catalogs"

    id: Mapped[int] = mapped_column(sa.BigInteger(), primary_key=True, autoincrement=True)
    guid: Mapped[str] = mapped_column(sa.String(36), unique=True)
    name: Mapped[str] = mapped_column(sa.String(255))
    page: Mapped[str] = mapped_column(sa.String(16), nullable=True)
    is_active: Mapped[bool]

    categories: Mapped[list["Category"]] = relationship("Category", back_populates="catalog")

    def __str__(self) -> str:
        return self.name
