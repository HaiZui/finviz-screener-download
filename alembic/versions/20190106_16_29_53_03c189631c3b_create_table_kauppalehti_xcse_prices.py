"""create_table_kauppalehti_xcse_prices

Revision ID: 03c189631c3b
Revises: fc9531b7146b
Create Date: 2019-01-06 16:29:53.652712

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '03c189631c3b'
down_revision = 'fc9531b7146b'
branch_labels = None
depends_on = None


def upgrade():
        connection = op.get_bind()
        connection.execute("""
                            CREATE TABLE kauppalehti.xcse_prices (
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
                            DROP table kauppalehti.xcse_prices
                            """)

