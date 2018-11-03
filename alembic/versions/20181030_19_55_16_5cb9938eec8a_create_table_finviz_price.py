"""create_table_finviz_price

Revision ID: 5cb9938eec8a
Revises: 71fa2e7676c3
Create Date: 2018-10-30 19:55:16.192331

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5cb9938eec8a'
down_revision = '71fa2e7676c3'
branch_labels = None
depends_on = None



def upgrade():
    connection = op.get_bind()
    connection.execute("""
                    CREATE TABLE finviz.price (
                    `Valid_From` decimal(18,8),
                    `Valid_To` decimal(18,8),
                      `Ticker` varchar(16) DEFAULT NULL,
                      `Price` varchar(16) DEFAULT NULL,
                      `Change` varchar(16) DEFAULT NULL,
                      `Volume` varchar(16) DEFAULT NULL,
                      `Timestamp` varchar(20) DEFAULT NULL,
                      `Sha256` varbinary(256) DEFAULT NULL
                    ) ENGINE=InnoDB DEFAULT CHARSET=latin1;

                        """)


def downgrade():
    connection = op.get_bind()
    connection.execute("""
                        DROP table finviz.price
                        """)

