"""work with promotions

Revision ID: 977d2f7c0fd5
Revises: 46a184094ef4
Create Date: 2023-02-16 12:19:46.277006

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "977d2f7c0fd5"
down_revision = "46a184094ef4"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("promotions", "date_start", existing_type=sa.DATE(), nullable=False)
    op.alter_column("promotions", "date_end", existing_type=sa.DATE(), nullable=False)
    op.alter_column(
        "promotions",
        "description",
        existing_type=sa.VARCHAR(length=100),
        type_=sa.VARCHAR(length=500),
        nullable=False,
    )
    # ### end Al
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("promotions", "date_end", existing_type=sa.DATE(), nullable=True)
    op.alter_column("promotions", "date_start", existing_type=sa.DATE(), nullable=True)
    op.alter_column(
        "promotions",
        "description",
        existing_type=sa.VARCHAR(length=500),
        type_=sa.VARCHAR(length=100),
        nullable=False,
    )
    # ### end Alembic commands ###