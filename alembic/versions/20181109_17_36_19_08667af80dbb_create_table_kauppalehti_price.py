"""create_table_kauppalehti_price

Revision ID: 08667af80dbb
Revises: b8bd59679090
Create Date: 2018-11-09 17:36:19.420852

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '08667af80dbb'
down_revision = 'b8bd59679090'
branch_labels = None
depends_on = None



def upgrade():
        connection = op.get_bind()
        connection.execute("""
                            CREATE TABLE kauppalehti.price (
	                    `Valid_From` decimal(18,8),
	                    `Valid_To` decimal(18,8),
                            `Nimi` varchar(255) DEFAULT NULL,
                            `Viim` varchar(16) DEFAULT NULL,
                            `Muutos` varchar(16) DEFAULT NULL,
                            `Aika` varchar(16) DEFAULT NULL,
                            `Osto` varchar(16) DEFAULT NULL,
                            `Myynti` varchar(16) DEFAULT NULL,
                            `Ylin` varchar(16) DEFAULT NULL,
                            `Alin` varchar(16) DEFAULT NULL,
                            `MiljE` varchar(16) DEFAULT NULL,
                            `Porssi` varchar(16) DEFAULT NULL,
                            `Teollisuus` varchar(255) DEFAULT NULL,
                            `Timestamp` varchar(20) DEFAULT NULL,
                            `Sha256` varbinary(256) DEFAULT NULL
                            ) ENGINE=InnoDB DEFAULT CHARSET=latin1;
                            """)

def downgrade():
        connection = op.get_bind()
        connection.execute("""
                            DROP table kauppalehti.price
                            """)

