from unittest.mock import patch

from deribit_price_api.domain.ticker import Ticker
from deribit_price_api.integrations.deribit import DeribitClient
from mocks import create_aiohttp_session_mock


async def test_fetches_index_price_from_deribit(aiohttp_response):
    client_session, request_session = create_aiohttp_session_mock(aiohttp_response)
    with patch("deribit_price_api.integrations.deribit.aiohttp.ClientSession") as session_class:
        session_class.return_value = client_session
        price = await DeribitClient("https://deribit.example/api").get_index_price(Ticker.BTC)

    assert price == 65000.12
    assert request_session.get.call_args.args[0] == "https://deribit.example/api"
    assert request_session.get.call_args.kwargs["params"] == {"index_name": "btc_usd"}


async def test_fake_client_returns_configured_price(fake_deribit_client):
    assert await fake_deribit_client.get_index_price(Ticker.ETH) == 3000.10
