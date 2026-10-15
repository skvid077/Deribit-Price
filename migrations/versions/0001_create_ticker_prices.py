import sqlalchemy as sa
from alembic import op

revision = "0001_create_ticker_prices"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "ticker_prices",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("ticker", sa.String(length=10), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("timestamp", sa.BigInteger(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_ticker_prices_ticker", "ticker_prices", ["ticker"])
    op.create_index("ix_ticker_prices_timestamp", "ticker_prices", ["timestamp"])


def downgrade() -> None:
    op.drop_index("ix_ticker_prices_timestamp", table_name="ticker_prices")
    op.drop_index("ix_ticker_prices_ticker", table_name="ticker_prices")
    op.drop_table("ticker_prices")
