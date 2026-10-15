from sqlalchemy import BigInteger, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from deribit_price_api.infrastructure.database import Base


class TickerPrice(Base):
    __tablename__ = "ticker_prices"

    id: Mapped[int] = mapped_column(primary_key=True)
    ticker: Mapped[str] = mapped_column(String(10), index=True)
    price: Mapped[float] = mapped_column(Float)
    timestamp: Mapped[int] = mapped_column(BigInteger, index=True)
