"""create_schema_analysis

Revision ID: eef4318b94b0
Revises: 99dc472fb237
Create Date: 2019-01-06 21:46:50.749902

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eef4318b94b0'
down_revision = '99dc472fb237'
branch_labels = None
depends_on = None


def upgrade():
    connection = op.get_bind()
    connection.execute("""
                        CREATE schema analysis
                        """)


def downgrade():
    connection = op.get_bind()
    connection.execute("""
                        DROP schema analysis
                        """)
