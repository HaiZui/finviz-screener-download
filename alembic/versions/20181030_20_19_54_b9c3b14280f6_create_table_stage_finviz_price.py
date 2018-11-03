"""create_table_stage_finviz_price

Revision ID: b9c3b14280f6
Revises: 5cb9938eec8a
Create Date: 2018-10-30 20:19:54.522210

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9c3b14280f6'
down_revision = '5cb9938eec8a'
branch_labels = None
depends_on = None


def upgrade():
    connection = op.get_bind()
    connection.execute("""
                    CREATE TABLE stage.finviz_price (
                      `Ticker` varchar(255) DEFAULT NULL,
                      `Price` varchar(255) DEFAULT NULL,
                      `Change` varchar(255) DEFAULT NULL,
                      `Volume` varchar(255) DEFAULT NULL,
                      `Timestamp` varchar(20) DEFAULT NULL,
                      `Sha256` varbinary(256) DEFAULT NULL
                    ) ENGINE=InnoDB DEFAULT CHARSET=latin1;

                        """)


def downgrade():
    connection = op.get_bind()
    connection.execute("""
                        DROP table stage.finviz_price
                        """)
