"""renamed message in callbacks.

Revision ID: 3b383c106c61
Revises: 74b3c392d767
Create Date: 2022-10-17 13:00:25.249522

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "3b383c106c61"
down_revision = "74b3c392d767"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("callbacks", sa.Column("message", sa.Text(), nullable=True))
    op.drop_column("callbacks", "description")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "callbacks", sa.Column("description", sa.TEXT(), autoincrement=False, nullable=True)
    )
    op.drop_column("callbacks", "message")
    # ### end Alembic commands ###
