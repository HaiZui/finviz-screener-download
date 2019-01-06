"""create_table_stage_kauppalehti_xcse_prices

Revision ID: fc9531b7146b
Revises: a25c5a739104
Create Date: 2019-01-06 16:29:46.958123

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc9531b7146b'
down_revision = 'a25c5a739104'
branch_labels = None
depends_on = None


def upgrade():
        connection = op.get_bind()
        connection.execute("""
                            CREATE TABLE stage.kauppalehti_xcse_prices (
                            `closePrice` varchar(255) DEFAULT NULL,
                            `marketValue` varchar(255) DEFAULT NULL,
                            `tradeCurrency` varchar(255) DEFAULT NULL,
                            `tickSize` varchar(255) DEFAULT NULL,
                            `company` varchar(255) DEFAULT NULL,
                            `closeDateTime` varchar(255) DEFAULT NULL,
                            `insRef` varchar(255) DEFAULT NULL,
                            `internalTurnover` varchar(255) DEFAULT NULL,
                            `isin` varchar(255) DEFAULT NULL,
                            `internalQuantity` varchar(255) DEFAULT NULL,
                            `name` varchar(255) DEFAULT NULL,
                            `quantity` varchar(255) DEFAULT NULL,
                            `turnover` varchar(255) DEFAULT NULL,
                            `dayLowPrice` varchar(255) DEFAULT NULL,
                            `lastPrice` varchar(255) DEFAULT NULL,
                            `openPrice` varchar(255) DEFAULT NULL,
                            `dayHighPrice` varchar(255) DEFAULT NULL,
                            `changePercent1m` varchar(255) DEFAULT NULL,
                            `askPrice` varchar(255) DEFAULT NULL,
                            `changePercent` varchar(255) DEFAULT NULL,
                            `bidPrice` varchar(255) DEFAULT NULL,
                            `symbol` varchar(255) DEFAULT NULL,
                            `numberOfShares` varchar(255) DEFAULT NULL,
                            `totalCompanyShares` varchar(255) DEFAULT NULL,
                            `Timestamp` varchar(20) DEFAULT NULL,
                            `Sha256` varbinary(256) DEFAULT NULL
                            ) ENGINE=InnoDB DEFAULT CHARSET=latin1;
                            """)

def downgrade():
        connection = op.get_bind()
        connection.execute("""
                            DROP table stage.kauppalehti_xcse_prices
                            """)
