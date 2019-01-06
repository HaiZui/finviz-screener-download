"""create_table_analysis_dates

Revision ID: f02f21d00582
Revises: eef4318b94b0
Create Date: 2019-01-06 21:47:02.742717

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f02f21d00582'
down_revision = 'eef4318b94b0'
branch_labels = None
depends_on = None



def upgrade():
        op.create_table("dates"
                        , sa.Column('ID', sa.Integer, primary_key=True)
                        , sa.Column('date', sa.Date)
                        , sa.Column('is_business_day', sa.Boolean)
                        , schema = 'analysis')
        

def downgrade():
        op.drop_table('dates', schema='analysis')
