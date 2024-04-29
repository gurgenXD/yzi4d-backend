"""Changed callbacks..

Revision ID: cc26a3e9bfb6
Revises: 11ef79646f2f
Create Date: 2024-04-15 14:43:46.566058

"""

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "cc26a3e9bfb6"
down_revision = "11ef79646f2f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("callbacks", "message")
    op.drop_column("callbacks", "name")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("callbacks", sa.Column("name", sa.VARCHAR(length=100), autoincrement=False, nullable=False))
    op.add_column("callbacks", sa.Column("message", sa.TEXT(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
