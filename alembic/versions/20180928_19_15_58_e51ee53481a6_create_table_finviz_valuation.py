"""create_table_finviz_valuation

Revision ID: e51ee53481a6
Revises: f61a21bf83e4
Create Date: 2018-09-28 19:15:58.997370

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e51ee53481a6'
down_revision = 'f61a21bf83e4'
branch_labels = None
depends_on = None


def upgrade():
    connection = op.get_bind()
    connection.execute("""
                    CREATE TABLE finviz.valuation (
                    `Valid_From` float,
                    `Valid_To` float,
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
                      `Timestamp` float DEFAULT NULL,
                      `Sha256` varbinary(256) DEFAULT NULL
                    ) ENGINE=InnoDB DEFAULT CHARSET=latin1;

                        """)


def downgrade():
    connection = op.get_bind()
    connection.execute("""
                        DROP table finviz.valuation
                        """)

