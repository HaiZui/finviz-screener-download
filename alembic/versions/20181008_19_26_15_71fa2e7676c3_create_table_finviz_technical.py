"""create_table_finviz_technical

Revision ID: 71fa2e7676c3
Revises: f39cc587d027
Create Date: 2018-10-08 19:26:15.433148

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '71fa2e7676c3'
down_revision = 'f39cc587d027'
branch_labels = None
depends_on = None



def upgrade():
    connection = op.get_bind()
    connection.execute("""
                    CREATE TABLE finviz.technical (
                    `Valid_From` decimal(18,8),
                    `Valid_To` decimal(18,8),
                      `Ticker` varchar(16) DEFAULT NULL,
                      `Beta` varchar(16) DEFAULT NULL,
                      `ATR` varchar(16) DEFAULT NULL,
                      `SMA20` varchar(16) DEFAULT NULL,
                      `SMA50` varchar(16) DEFAULT NULL,
                      `SMA200` varchar(16) DEFAULT NULL,
                      `52W High` varchar(16) DEFAULT NULL,
                      `52W Low` varchar(16) DEFAULT NULL,
                      `RSI` varchar(16) DEFAULT NULL,
                      `Price` varchar(16) DEFAULT NULL,
                      `Change` varchar(16) DEFAULT NULL,
                      `from Open` varchar(16) DEFAULT NULL,
                      `Gap` varchar(16) DEFAULT NULL,
                      `Volume` varchar(16) DEFAULT NULL,
                      `Timestamp` varchar(20) DEFAULT NULL,
                      `Sha256` varbinary(256) DEFAULT NULL
                      ) ENGINE=InnoDB DEFAULT CHARSET=latin1;

                        """)


def downgrade():
    connection = op.get_bind()
    connection.execute("""
                        DROP table finviz.technical
                        """)
