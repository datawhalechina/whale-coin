"""1015 modify order2total_order

Revision ID: 6b4a09ad3ea1
Revises: 28c53d12921c
Create Date: 2024-10-15 19:41:51.091565

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = "6b4a09ad3ea1"
down_revision: Union[str, None] = "28c53d12921c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "github_repos",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("username", sa.VARCHAR(length=200), nullable=False),
        sa.Column("repo_name", sa.VARCHAR(length=200), nullable=False),
        sa.Column("contributors", sa.VARCHAR(length=200), nullable=False),
        sa.Column("create_time", sa.DateTime(), nullable=True),
        sa.Column("update_time", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "total_order",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("itemid", sa.Integer(), nullable=True),
        sa.Column("quantity", sa.Integer(), nullable=True),
        sa.Column("order_type", sa.VARCHAR(length=200), nullable=True),
        sa.Column("status", sa.VARCHAR(length=1), nullable=True),
        sa.Column("toal_price", sa.Float(), nullable=True),
        sa.Column("address", sa.VARCHAR(length=1000), nullable=True),
        sa.Column("phone", sa.Integer(), nullable=True),
        sa.Column("create_time", sa.DateTime(), nullable=True),
        sa.Column("audit_id", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.drop_table("order")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "order",
        sa.Column("id", mysql.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("user_id", mysql.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("itemid", mysql.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("quantity", mysql.INTEGER(), autoincrement=False, nullable=True),
        sa.Column(
            "order_type",
            mysql.VARCHAR(collation="utf8mb4_general_ci", length=200),
            nullable=True,
        ),
        sa.Column(
            "status",
            mysql.VARCHAR(collation="utf8mb4_general_ci", length=1),
            nullable=True,
        ),
        sa.Column("toal_price", mysql.FLOAT(), nullable=True),
        sa.Column(
            "address",
            mysql.VARCHAR(collation="utf8mb4_general_ci", length=1000),
            nullable=True,
        ),
        sa.Column("create_time", mysql.DATETIME(), nullable=True),
        sa.Column("phone", mysql.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("audit_id", mysql.INTEGER(), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint("id"),
        mysql_collate="utf8mb4_general_ci",
        mysql_default_charset="utf8mb4",
        mysql_engine="InnoDB",
    )
    op.drop_table("total_order")
    op.drop_table("github_repos")
    # ### end Alembic commands ###
