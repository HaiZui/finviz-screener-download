"""create_table_stage_finviz_technical

Revision ID: f39cc587d027
Revises: aab919887618
Create Date: 2018-10-08 19:26:11.099039

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f39cc587d027'
down_revision = 'aab919887618'
branch_labels = None
depends_on = None



def upgrade():
    connection = op.get_bind()
    connection.execute("""
                    CREATE TABLE stage.finviz_technical (
                      `Ticker` varchar(255) DEFAULT NULL,
                      `Beta` varchar(255) DEFAULT NULL,
                      `ATR` varchar(255) DEFAULT NULL,
                      `SMA20` varchar(255) DEFAULT NULL,
                      `SMA50` varchar(255) DEFAULT NULL,
                      `SMA200` varchar(255) DEFAULT NULL,
                      `52W High` varchar(255) DEFAULT NULL,
                      `52W Low` varchar(255) DEFAULT NULL,
                      `RSI` varchar(255) DEFAULT NULL,
                      `Price` varchar(255) DEFAULT NULL,
                      `Change` varchar(255) DEFAULT NULL,
                      `from Open` varchar(255) DEFAULT NULL,
                      `Gap` varchar(255) DEFAULT NULL,
                      `Volume` varchar(255) DEFAULT NULL,
                      `Timestamp` varchar(255) DEFAULT NULL,
                      `Sha256` varbinary(256) DEFAULT NULL
                      ) ENGINE=InnoDB DEFAULT CHARSET=latin1;

                        """)


def downgrade():
    connection = op.get_bind()
    connection.execute("""
                        DROP table stage.finviz_technical
                        """)
