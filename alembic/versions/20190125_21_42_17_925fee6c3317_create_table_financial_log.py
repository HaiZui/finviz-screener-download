"""create_table_financial_log

Revision ID: 925fee6c3317
Revises: cc39538dba7b
Create Date: 2019-01-25 21:42:17.727851

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '925fee6c3317'
down_revision = 'cc39538dba7b'
branch_labels = None
depends_on = None



def upgrade():
        op.create_table("log"
                        , sa.Column('ID', sa.Integer, primary_key=True)
                        , sa.Column('Timestamp', sa.VARCHAR(32))
                        , sa.Column('Caller', sa.VARCHAR(128))
                        , sa.Column('SchemaName', sa.VARCHAR(32))
                        , sa.Column('TableName', sa.VARCHAR(32))
                        , sa.Column('Action', sa.VARCHAR(32))
                        , sa.Column('RowCount', sa.Integer)
                        , sa.Column('Description', sa.types.Text)
                        , schema = 'financial')
        

def downgrade():
        op.drop_table('log', schema='financial')

