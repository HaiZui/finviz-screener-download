"""create_table_stage_valuation

Revision ID: 2bfe6d98e6d7
Revises: e51ee53481a6
Create Date: 2018-09-28 22:27:11.899697

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2bfe6d98e6d7'
down_revision = 'e51ee53481a6'
branch_labels = None
depends_on = None



def upgrade():
    connection = op.get_bind()
    connection.execute("""
                    CREATE TABLE stage.valuation (
                      `Ticker` varchar(16) DEFAULT NULL,
                      `Market Cap` varchar(16) DEFAULT NULL,
                      `P/E` varchar(16) DEFAULT NULL,
                      `Fwd P/E` varchar(16) DEFAULT NULL,
                      `PEG` varchar(16) DEFAULT NULL,
                      `P/S` varchar(16) DEFAULT NULL,
                      `P/B` varchar(16) DEFAULT NULL,
                      `P/C` varchar(16) DEFAULT NULL,
                      `P/FCF` varchar(16) DEFAULT NULL,
                      `EPS this Y` varchar(16) DEFAULT NULL,
                      `EPS next Y` varchar(16) DEFAULT NULL,
                      `EPS past 5Y` varchar(16) DEFAULT NULL,
                      `EPS next 5Y` varchar(16) DEFAULT NULL,
                      `Sales past 5Y` varchar(16) DEFAULT NULL,
                      `Timestamp` varchar(32) DEFAULT NULL,
                      `Sha256` varbinary(256) DEFAULT NULL
                    ) ENGINE=InnoDB DEFAULT CHARSET=latin1;

                        """)


def downgrade():
    connection = op.get_bind()
    connection.execute("""
                        DROP table stage.valuation
                        """)
