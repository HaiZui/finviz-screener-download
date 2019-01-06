"""create_table_kauppalehti_fnfi_prices

Revision ID: 99dc472fb237
Revises: 38e82ab1d01c
Create Date: 2019-01-06 16:30:17.055618

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '99dc472fb237'
down_revision = '38e82ab1d01c'
branch_labels = None
depends_on = None



def upgrade():
        connection = op.get_bind()
        connection.execute("""
                            CREATE TABLE kauppalehti.fnfi_prices (
	                    `Valid_From` decimal(18,8),
	                    `Valid_To` decimal(18,8),
                            `closePrice` varchar(32) DEFAULT NULL,
                            `marketValue` varchar(32) DEFAULT NULL,
                            `tradeCurrency` varchar(32) DEFAULT NULL,
                            `tickSize` varchar(32) DEFAULT NULL,
                            `company` varchar(32) DEFAULT NULL,
                            `closeDateTime` varchar(32) DEFAULT NULL,
                            `insRef` varchar(32) DEFAULT NULL,
                            `internalTurnover` varchar(32) DEFAULT NULL,
                            `isin` varchar(32) DEFAULT NULL,
                            `internalQuantity` varchar(32) DEFAULT NULL,
                            `name` varchar(128) DEFAULT NULL,
                            `quantity` varchar(32) DEFAULT NULL,
                            `turnover` varchar(32) DEFAULT NULL,
                            `dayLowPrice` varchar(32) DEFAULT NULL,
                            `lastPrice` varchar(32) DEFAULT NULL,
                            `openPrice` varchar(32) DEFAULT NULL,
                            `dayHighPrice` varchar(32) DEFAULT NULL,
                            `changePercent1m` varchar(32) DEFAULT NULL,
                            `askPrice` varchar(32) DEFAULT NULL,
                            `changePercent` varchar(32) DEFAULT NULL,
                            `bidPrice` varchar(32) DEFAULT NULL,
                            `symbol` varchar(32) DEFAULT NULL,
                            `numberOfShares` varchar(32) DEFAULT NULL,
                            `totalCompanyShares` varchar(32) DEFAULT NULL,
                            `Timestamp` varchar(32) DEFAULT NULL,
                            `Sha256` varbinary(256) DEFAULT NULL
                            ) ENGINE=InnoDB DEFAULT CHARSET=latin1;
                            """)

def downgrade():
        connection = op.get_bind()
        connection.execute("""
                            DROP table kauppalehti.fnfi_prices
                            """)
