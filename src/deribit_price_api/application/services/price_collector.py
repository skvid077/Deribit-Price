import asyncio

from deribit_price_api.application.ports import IndexPriceClient, PriceWriter
from deribit_price_api.domain.price import Price
from deribit_price_api.domain.ticker import Ticker


class PriceCollector:
    def __init__(self, client: IndexPriceClient, repository: PriceWriter) -> None:
        self._client = client
        self._repository = repository

    async def collect(self, timestamp: int) -> None:
        btc_price, eth_price = await asyncio.gather(
            self._client.get_index_price(Ticker.BTC),
            self._client.get_index_price(Ticker.ETH),
        )
        await self._repository.add_many([
            Price(Ticker.BTC, btc_price, timestamp),
            Price(Ticker.ETH, eth_price, timestamp),
        ])

