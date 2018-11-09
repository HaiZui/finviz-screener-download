"""create_schema_kauppalehti

Revision ID: e2958afb8f26
Revises: b9c3b14280f6
Create Date: 2018-11-09 17:45:54.079919

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2958afb8f26'
down_revision = 'b9c3b14280f6'
branch_labels = None
depends_on = None

def upgrade():
    connection = op.get_bind()
    connection.execute("""
                        CREATE schema kauppalehti
                        """)


def downgrade():
    connection = op.get_bind()
    connection.execute("""
                        DROP schema kauppalehti
                        """)
