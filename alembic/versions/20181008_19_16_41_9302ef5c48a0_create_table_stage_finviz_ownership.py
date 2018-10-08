"""create_table_stage_finviz_ownership

Revision ID: 9302ef5c48a0
Revises: 25ec5c34c8bd
Create Date: 2018-10-08 19:16:41.411157

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9302ef5c48a0'
down_revision = '25ec5c34c8bd'
branch_labels = None
depends_on = None



def upgrade():
    connection = op.get_bind()
    connection.execute("""
                    CREATE TABLE stage.finviz_ownership (
                      `Ticker` varchar(255) DEFAULT NULL,
                      `Market Cap` varchar(255) DEFAULT NULL,
                      `Outstanding` varchar(255) DEFAULT NULL,
                      `Float` varchar(255) DEFAULT NULL,
                      `Insider Own` varchar(255) DEFAULT NULL,
                      `Insider Trans` varchar(255) DEFAULT NULL,
                      `Inst Own` varchar(255) DEFAULT NULL,
                      `Inst Trans` varchar(255) DEFAULT NULL,
                      `Float Short` varchar(255) DEFAULT NULL,
                      `Short Ratio` varchar(255) DEFAULT NULL,
                      `Avg Volume` varchar(255) DEFAULT NULL,
                      `Price` varchar(255) DEFAULT NULL,
                      `Change` varchar(255) DEFAULT NULL,
                      `Volume` varchar(255) DEFAULT NULL,
                      `Timestamp` varchar(255) DEFAULT NULL,
                      `Sha256` varbinary(256) DEFAULT NULL
                      ) ENGINE=InnoDB DEFAULT CHARSET=latin1;

                        """)


def downgrade():
    connection = op.get_bind()
    connection.execute("""
                        DROP table stage.finviz_ownership
                        """)
