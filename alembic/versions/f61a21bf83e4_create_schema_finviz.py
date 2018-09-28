"""create_schema_finviz

Revision ID: f61a21bf83e4
Revises: 
Create Date: 2018-09-28 19:01:09.498383

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f61a21bf83e4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    connection = op.get_bind()
    connection.execute("""
                        CREATE schema finviz
                        """)


def downgrade():
    connection = op.get_bind()
    connection.execute("""
                        DROP schema finviz
                        """)

