"""office4.

Revision ID: 3813bc49ebc7
Revises: 2f0eaea88e68
Create Date: 2022-12-25 15:54:08.303197

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "3813bc49ebc7"
down_revision = "2f0eaea88e68"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "offices",
        sa.Column("main_doctor", sa.String(length=50), nullable=False, server_default="0"),
    )
    op.add_column(
        "offices",
        sa.Column(
            "main_doctor_work_time", sa.String(length=50), nullable=False, server_default="0"
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("offices", "main_doctor_work_time")
    op.drop_column("offices", "main_doctor")
    # ### end Alembic commands ###
