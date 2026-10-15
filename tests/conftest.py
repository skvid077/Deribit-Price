import pytest
from unittest.mock import MagicMock

from deribit_price_api.domain.ticker import Ticker
from fakes import FakeDeribitClient
from mocks import create_aiohttp_response_mock, create_session_mock


@pytest.fixture
def mocked_session() -> MagicMock:
    return create_session_mock()


@pytest.fixture
def deribit_prices() -> dict[Ticker, float]:
    return {Ticker.BTC: 65000.12, Ticker.ETH: 3000.10}


@pytest.fixture
def fake_deribit_client(deribit_prices: dict[Ticker, float]) -> FakeDeribitClient:
    return FakeDeribitClient(deribit_prices)


@pytest.fixture
def aiohttp_response() -> MagicMock:
    return create_aiohttp_response_mock(65000.12)
