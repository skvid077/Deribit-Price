import collections.abc as cabc

from deribit_price_api.domain.price import Price
from deribit_price_api.domain.ticker import Ticker


class FakeDeribitClient:
    def __init__(self, prices: cabc.Mapping[Ticker, float]) -> None:
        self._prices = prices

    async def get_index_price(self, ticker: Ticker) -> float:
        return self._prices[ticker]


class FakePriceWriter:
    def __init__(self) -> None:
        self.prices: list[Price] = []

    async def add_many(self, prices: cabc.Iterable[Price]) -> None:
        self.prices.extend(prices)
