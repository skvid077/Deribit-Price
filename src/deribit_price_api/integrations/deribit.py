import aiohttp

from deribit_price_api.domain.ticker import Ticker


class DeribitClient:
    def __init__(self, api_url: str) -> None:
        self._api_url = api_url

    async def get_index_price(self, ticker: Ticker) -> float:
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(self._api_url, params={"index_name": f"{ticker}_usd"}) as response:
                response.raise_for_status()
                payload = await response.json()
        return float(payload["result"]["index_price"])
