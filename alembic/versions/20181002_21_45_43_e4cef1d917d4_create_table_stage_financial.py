"""create_table_stage_financial

Revision ID: e4cef1d917d4
Revises: 2bfe6d98e6d7
Create Date: 2018-10-02 21:45:43.123886

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e4cef1d917d4'
down_revision = '2bfe6d98e6d7'
branch_labels = None
depends_on = None



def upgrade():
    connection = op.get_bind()
    connection.execute("""
                    CREATE TABLE stage.financial (
                      `Ticker` varchar(255) DEFAULT NULL,
                      `Market Cap` varchar(255) DEFAULT NULL,
                      `Dividend` varchar(255) DEFAULT NULL,
                      `ROA` varchar(255) DEFAULT NULL,
                      `ROE` varchar(255) DEFAULT NULL,
                      `ROI` varchar(255) DEFAULT NULL,
                      `Curr R` varchar(255) DEFAULT NULL,
                      `Quick R` varchar(255) DEFAULT NULL,
                      `LTDebt/Eq` varchar(255) DEFAULT NULL,
                      `Debt/Eq` varchar(255) DEFAULT NULL,
                      `Gross M` varchar(255) DEFAULT NULL,
                      `Oper M` varchar(255) DEFAULT NULL,
                      `Profit M` varchar(255) DEFAULT NULL,
                      `Earnings` varchar(255) DEFAULT NULL,
                      `Timestamp` varchar(255) DEFAULT NULL,
                      `Sha256` varbinary(256) DEFAULT NULL
                      ) ENGINE=InnoDB DEFAULT CHARSET=latin1;

                        """)


def downgrade():
    connection = op.get_bind()
    connection.execute("""
                        DROP table stage.financial
                        """)