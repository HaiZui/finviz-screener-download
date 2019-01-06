"""create_table_analysis_times

Revision ID: cc39538dba7b
Revises: f02f21d00582
Create Date: 2019-01-06 21:50:37.582583

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cc39538dba7b'
down_revision = 'f02f21d00582'
branch_labels = None
depends_on = None



def upgrade():
        op.create_table('times'
                        , sa.Column('ID', sa.Integer, primary_key=True)
                        , sa.Column('hour', sa.Integer)
                        , sa.Column('minute', sa.Integer)
                        , sa.Column('second', sa.Integer)
                        , sa.Column('is_business_hour', sa.Boolean)
                        , schema = 'analysis')
        

def downgrade():
        op.drop_table('times', schema='analysis')
