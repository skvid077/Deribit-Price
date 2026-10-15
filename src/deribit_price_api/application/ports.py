import collections.abc as cabc
import typing as tp

from deribit_price_api.domain.price import Price
from deribit_price_api.domain.ticker import Ticker


class IndexPriceClient(tp.Protocol):
    async def get_index_price(self, ticker: Ticker) -> float: ...


class PriceWriter(tp.Protocol):
    async def add_many(self, prices: cabc.Iterable[Price]) -> None: ...
