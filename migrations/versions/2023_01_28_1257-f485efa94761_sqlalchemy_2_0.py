"""sqlalchemy 2.0.

Revision ID: f485efa94761
Revises: c897cf1f6b25
Create Date: 2023-01-28 12:57:40.794661

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "f485efa94761"
down_revision = "c897cf1f6b25"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("analyzes", "is_active", existing_type=sa.BOOLEAN(), nullable=False)
    op.alter_column("callbacks", "answered", existing_type=sa.BOOLEAN(), nullable=False)
    op.alter_column("news", "is_active", existing_type=sa.BOOLEAN(), nullable=False)
    op.alter_column("offices", "city_id", existing_type=sa.BIGINT(), nullable=False)
    op.alter_column("pages", "is_active", existing_type=sa.BOOLEAN(), nullable=False)
    op.alter_column("promotions", "is_active", existing_type=sa.BOOLEAN(), nullable=False)
    op.alter_column("promotions", "on_main", existing_type=sa.BOOLEAN(), nullable=False)
    op.alter_column("services", "service_type_id", existing_type=sa.BIGINT(), nullable=False)
    op.alter_column("services", "is_active", existing_type=sa.BOOLEAN(), nullable=False)
    op.alter_column("services", "on_main", existing_type=sa.BOOLEAN(), nullable=False)
    op.alter_column("services_types", "on_main", existing_type=sa.BOOLEAN(), nullable=False)
    op.add_column("specialists", sa.Column("titles", sa.Text(), nullable=True))
    op.alter_column("specialists", "patronymic", existing_type=sa.VARCHAR(length=50), nullable=True)
    op.alter_column("specialists", "on_main", existing_type=sa.BOOLEAN(), nullable=False)
    op.alter_column("specialists", "is_active", existing_type=sa.BOOLEAN(), nullable=False)
    op.drop_column("specialists", "titules")
    op.alter_column("users", "username", existing_type=sa.VARCHAR(length=64), nullable=False)
    op.alter_column("users", "email", existing_type=sa.VARCHAR(length=64), nullable=False)
    op.alter_column("users", "is_active", existing_type=sa.BOOLEAN(), nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("users", "is_active", existing_type=sa.BOOLEAN(), nullable=True)
    op.alter_column("users", "email", existing_type=sa.VARCHAR(length=64), nullable=True)
    op.alter_column("users", "username", existing_type=sa.VARCHAR(length=64), nullable=True)
    op.add_column(
        "specialists", sa.Column("titules", sa.TEXT(), autoincrement=False, nullable=True)
    )
    op.alter_column("specialists", "is_active", existing_type=sa.BOOLEAN(), nullable=True)
    op.alter_column("specialists", "on_main", existing_type=sa.BOOLEAN(), nullable=True)
    op.alter_column("specialists", "patronymic", existing_type=sa.VARCHAR(length=50), nullable=True)
    op.drop_column("specialists", "titles")
    op.alter_column("services_types", "on_main", existing_type=sa.BOOLEAN(), nullable=True)
    op.alter_column("services", "on_main", existing_type=sa.BOOLEAN(), nullable=True)
    op.alter_column("services", "is_active", existing_type=sa.BOOLEAN(), nullable=True)
    op.alter_column("services", "service_type_id", existing_type=sa.BIGINT(), nullable=True)
    op.alter_column("promotions", "on_main", existing_type=sa.BOOLEAN(), nullable=True)
    op.alter_column("promotions", "is_active", existing_type=sa.BOOLEAN(), nullable=True)
    op.alter_column("pages", "is_active", existing_type=sa.BOOLEAN(), nullable=True)
    op.alter_column("offices", "city_id", existing_type=sa.BIGINT(), nullable=True)
    op.alter_column("news", "is_active", existing_type=sa.BOOLEAN(), nullable=True)
    op.alter_column("callbacks", "answered", existing_type=sa.BOOLEAN(), nullable=True)
    op.alter_column("analyzes", "is_active", existing_type=sa.BOOLEAN(), nullable=True)
    # ### end Alembic commands ###
