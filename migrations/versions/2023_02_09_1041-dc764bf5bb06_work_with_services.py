"""work with services

Revision ID: dc764bf5bb06
Revises: aa11cc4ab6e7
Create Date: 2023-02-09 10:41:10.017516

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "dc764bf5bb06"
down_revision = "aa11cc4ab6e7"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("services", sa.Column("description", sa.Text(), nullable=False))
    op.alter_column("specialists", "can_online", existing_type=sa.BOOLEAN(), nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("specialists", "can_online", existing_type=sa.BOOLEAN(), nullable=True)
    op.drop_column("services", "description")
    # ### end Alembic commands ###
