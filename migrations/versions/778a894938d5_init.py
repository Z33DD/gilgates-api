"""init

Revision ID: 778a894938d5
Revises: 
Create Date: 2023-02-02 23:01:35.503582

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "778a894938d5"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user",
        sa.Column("uid", sa.CHAR(length=32), nullable=False),
        sa.Column("created_at", sa.DATETIME(), nullable=False),
        sa.Column("updated_at", sa.DATETIME(), nullable=False),
        sa.Column("last_login", sa.DATETIME(), nullable=True),
        sa.Column("ative", sa.BOOLEAN(), nullable=True),
        sa.Column("password", sa.VARCHAR(), nullable=True),
        sa.Column("role", sa.VARCHAR(), nullable=False),
        sa.Column("name", sa.VARCHAR(), nullable=False),
        sa.Column("cpf", sa.VARCHAR(), nullable=True),
        sa.Column("email", sa.VARCHAR(), nullable=False),
        sa.Column("address_uid", sa.CHAR(length=32), nullable=True),
        sa.Column("company_id", sa.CHAR(length=32), nullable=True),
        sa.ForeignKeyConstraint(
            ["address_uid"],
            ["address.uid"],
        ),
        sa.ForeignKeyConstraint(
            ["company_id"],
            ["company.uid"],
        ),
        sa.PrimaryKeyConstraint("uid"),
    )
    op.create_table(
        "company",
        sa.Column("uid", sa.CHAR(length=32), nullable=False),
        sa.Column("created_at", sa.DATETIME(), nullable=False),
        sa.Column("updated_at", sa.DATETIME(), nullable=False),
        sa.Column("name", sa.VARCHAR(), nullable=False),
        sa.Column("cnpj", sa.VARCHAR(), nullable=False),
        sa.Column("address_uid", sa.CHAR(length=32), nullable=True),
        sa.ForeignKeyConstraint(
            ["address_uid"],
            ["address.uid"],
        ),
        sa.PrimaryKeyConstraint("uid"),
        sa.UniqueConstraint("cnpj"),
    )
    op.create_table(
        "customer",
        sa.Column("uid", sa.CHAR(length=32), nullable=False),
        sa.Column("created_at", sa.DATETIME(), nullable=False),
        sa.Column("updated_at", sa.DATETIME(), nullable=False),
        sa.Column("name", sa.VARCHAR(), nullable=False),
        sa.Column("phone", sa.VARCHAR(), nullable=False),
        sa.Column("employee_id", sa.CHAR(length=32), nullable=True),
        sa.Column("address_uid", sa.CHAR(length=32), nullable=True),
        sa.ForeignKeyConstraint(
            ["address_uid"],
            ["address.uid"],
        ),
        sa.ForeignKeyConstraint(
            ["employee_id"],
            ["user.uid"],
        ),
        sa.PrimaryKeyConstraint("uid"),
    )
    op.create_table(
        "address",
        sa.Column("uid", sa.CHAR(length=32), nullable=False),
        sa.Column("created_at", sa.DATETIME(), nullable=False),
        sa.Column("updated_at", sa.DATETIME(), nullable=False),
        sa.Column("lat", sa.FLOAT(), nullable=False),
        sa.Column("lng", sa.FLOAT(), nullable=False),
        sa.Column("city", sa.VARCHAR(), nullable=False),
        sa.Column("state", sa.VARCHAR(), nullable=False),
        sa.PrimaryKeyConstraint("uid"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("address")
    op.drop_table("customer")
    op.drop_table("company")
    op.drop_table("user")
    # ### end Alembic commands ###