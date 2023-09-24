import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.adapters.storage.db.base_model import BaseModel
from fastapi_storages.integrations.sqlalchemy import FileType


from fastapi_storages import FileSystemStorage
from utils.constants import MEDIA_DIR


categories_services_table = sa.Table(
    "categories_services_rel",
    BaseModel.metadata,
    sa.Column(
        "service_category_id",
        sa.ForeignKey("services_categories.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    sa.Column("service_id", sa.ForeignKey("services.id", ondelete="CASCADE"), primary_key=True),
)


class Service(BaseModel):
    """Услуги."""

    __tablename__ = "services"

    id: Mapped[str] = mapped_column(sa.String(36), primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(255))
    short_description: Mapped[str | None] = mapped_column(sa.String(255))
    description: Mapped[str | None] = mapped_column(sa.Text())
    preparation: Mapped[str | None] = mapped_column(sa.Text())
    ready_from: Mapped[int | None]
    ready_to: Mapped[int | None]
    is_active: Mapped[bool]

    categories: Mapped[list["ServiceCategory"]] = relationship(
        "ServiceCategory", secondary=categories_services_table, back_populates="services"
    )

    def __str__(self) -> str:
        return self.name


class ServiceCategory(BaseModel):
    """Категория услуг."""

    __tablename__ = "services_categories"

    id: Mapped[str] = mapped_column(sa.String(36), primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(255))
    icon: Mapped[str | None] = mapped_column(
        FileType(storage=FileSystemStorage(path=str(MEDIA_DIR / "services_categories")))
    )
    is_active: Mapped[bool]

    parent_id: Mapped[str | None] = mapped_column(
        sa.String(36), sa.ForeignKey("services_categories.id", ondelete="SET NULL")
    )
    catalog_id: Mapped[str] = mapped_column(
        sa.String(36), sa.ForeignKey("services_catalogs.id", ondelete="CASCADE")
    )

    children: Mapped[list["ServiceCategory"]] = relationship(
        "ServiceCategory", back_populates="parent"
    )
    parent: Mapped["ServiceCategory"] = relationship(
        "ServiceCategory", back_populates="children", remote_side=[id]
    )
    catalog: Mapped["ServiceCatalog"] = relationship("ServiceCatalog", back_populates="categories")
    services: Mapped[list["Service"]] = relationship(
        "Service", secondary=categories_services_table, back_populates="categories"
    )

    def __str__(self) -> str:
        return self.name


class ServiceCatalog(BaseModel):
    """Каталог услуг."""

    __tablename__ = "services_catalogs"

    id: Mapped[str] = mapped_column(sa.String(36), primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(255))
    page: Mapped[str] = mapped_column(sa.String(16))
    is_active: Mapped[bool]

    categories: Mapped[list["ServiceCategory"]] = relationship(
        "ServiceCategory", back_populates="catalog"
    )

    def __str__(self) -> str:
        return self.name
