from dataclasses import dataclass

from deribit_price_api.domain.ticker import Ticker


@dataclass(frozen=True, slots=True)
class Price:
    ticker: Ticker
    value: float
    timestamp: int
