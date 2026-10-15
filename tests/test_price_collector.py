from deribit_price_api.application.services.price_collector import PriceCollector
from deribit_price_api.domain.ticker import Ticker
from fakes import FakePriceWriter


async def test_collects_both_prices_with_one_timestamp(fake_deribit_client) -> None:
    writer = FakePriceWriter()

    await PriceCollector(fake_deribit_client, writer).collect(1_704_067_200)

    assert writer.prices[0].ticker is Ticker.BTC
    assert writer.prices[0].timestamp == 1_704_067_200
    assert writer.prices[1].ticker is Ticker.ETH
    assert writer.prices[1].timestamp == 1_704_067_200
