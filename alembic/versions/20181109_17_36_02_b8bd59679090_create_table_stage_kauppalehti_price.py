"""create_table_stage_kauppalehti_price

Revision ID: b8bd59679090
Revises: e2958afb8f26
Create Date: 2018-11-09 17:36:02.323332

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b8bd59679090'
down_revision = 'e2958afb8f26'
branch_labels = None
depends_on = None

def upgrade():
        connection = op.get_bind()
        connection.execute("""
                            CREATE TABLE stage.kauppalehti_price (
                            `Nimi` varchar(255) DEFAULT NULL,
                            `Viim` varchar(255) DEFAULT NULL,
                            `Muutos` varchar(255) DEFAULT NULL,
                            `Aika` varchar(255) DEFAULT NULL,
                            `Osto` varchar(255) DEFAULT NULL,
                            `Myynti` varchar(255) DEFAULT NULL,
                            `Ylin` varchar(255) DEFAULT NULL,
                            `Alin` varchar(255) DEFAULT NULL,
                            `MiljE` varchar(255) DEFAULT NULL,
                            `Porssi` varchar(255) DEFAULT NULL,
                            `Teollisuus` varchar(255) DEFAULT NULL,
                            `Timestamp` varchar(20) DEFAULT NULL,
                            `Sha256` varbinary(256) DEFAULT NULL
                            ) ENGINE=InnoDB DEFAULT CHARSET=latin1;
                            """)

def downgrade():
        connection = op.get_bind()
        connection.execute("""
                            DROP table stage.kauppalehti_price
                            """)

