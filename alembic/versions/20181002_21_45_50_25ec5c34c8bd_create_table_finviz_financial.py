"""create_table_finviz_financial

Revision ID: 25ec5c34c8bd
Revises: e4cef1d917d4
Create Date: 2018-10-02 21:45:50.000475

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '25ec5c34c8bd'
down_revision = 'e4cef1d917d4'
branch_labels = None
depends_on = None



def upgrade():
    connection = op.get_bind()
    connection.execute("""
                    CREATE TABLE finviz.financial (
                    `Valid_From` decimal(18,8),
                    `Valid_To` decimal(18,8),
                      `Ticker` varchar(16) DEFAULT NULL,
                      `Market Cap` varchar(16) DEFAULT NULL,
                      `Dividend` varchar(16) DEFAULT NULL,
                      `ROA` varchar(16) DEFAULT NULL,
                      `ROE` varchar(16) DEFAULT NULL,
                      `ROI` varchar(16) DEFAULT NULL,
                      `Curr R` varchar(16) DEFAULT NULL,
                      `Quick R` varchar(16) DEFAULT NULL,
                      `LTDebt/Eq` varchar(16) DEFAULT NULL,
                      `Debt/Eq` varchar(16) DEFAULT NULL,
                      `Gross M` varchar(16) DEFAULT NULL,
                      `Oper M` varchar(16) DEFAULT NULL,
                      `Profit M` varchar(16) DEFAULT NULL,
                      `Earnings` varchar(16) DEFAULT NULL,
                      `Timestamp` varchar(20) DEFAULT NULL,
                      `Sha256` varbinary(256) DEFAULT NULL
                      ) ENGINE=InnoDB DEFAULT CHARSET=latin1;

                        """)


def downgrade():
    connection = op.get_bind()
    connection.execute("""
                        DROP table finviz.financial
                        """)
