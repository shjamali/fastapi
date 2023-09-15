"""create post table

Revision ID: 3ed25902cb71
Revises: 
Create Date: 2023-09-15 10:23:44.594293

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3ed25902cb71"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("title", sa.String(255)),
    )
    pass


def downgrade() -> None:
    op.drop("posts")
    pass
