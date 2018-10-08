"""create_table_finviz_ownership

Revision ID: aab919887618
Revises: 9302ef5c48a0
Create Date: 2018-10-08 19:16:50.274213

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aab919887618'
down_revision = '9302ef5c48a0'
branch_labels = None
depends_on = None


def upgrade():
    connection = op.get_bind()
    connection.execute("""
                    CREATE TABLE finviz.ownership (
                    `Valid_From` decimal(18,8),
                    `Valid_To` decimal(18,8),
                      `Ticker` varchar(16) DEFAULT NULL,
                      `Market Cap` varchar(16) DEFAULT NULL,
                      `Outstanding` varchar(16) DEFAULT NULL,
                      `Float` varchar(16) DEFAULT NULL,
                      `Insider Own` varchar(16) DEFAULT NULL,
                      `Insider Trans` varchar(16) DEFAULT NULL,
                      `Inst Own` varchar(16) DEFAULT NULL,
                      `Inst Trans` varchar(16) DEFAULT NULL,
                      `Float Short` varchar(16) DEFAULT NULL,
                      `Short Ratio` varchar(16) DEFAULT NULL,
                      `Avg Volume` varchar(16) DEFAULT NULL,
                      `Timestamp` varchar(20) DEFAULT NULL,
                      `Sha256` varbinary(256) DEFAULT NULL
                      ) ENGINE=InnoDB DEFAULT CHARSET=latin1;

                        """)


def downgrade():
    connection = op.get_bind()
    connection.execute("""
                        DROP table finviz.ownership
                        """)

