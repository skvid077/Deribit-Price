import collections.abc as cabc
import datetime as dt
from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

from deribit_price_api.domain.ticker import Ticker
from deribit_price_api.infrastructure.models import TickerPrice
from deribit_price_api.main import create_app
from deribit_price_api.presentation.api.prices import get_repository


@pytest.fixture
async def api_client() -> cabc.AsyncIterator[tuple[httpx.AsyncClient, MagicMock]]:
    application = create_app()
    repository = MagicMock()
    repository.get_all_for_ticker = AsyncMock()
    repository.get_latest = AsyncMock()
    repository.get_all_for_date = AsyncMock()
    application.dependency_overrides[get_repository] = lambda: repository
    transport = httpx.ASGITransport(app=application)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client, repository


async def test_get_prices_requires_ticker(api_client: tuple[httpx.AsyncClient, MagicMock]) -> None:
    client, _ = api_client

    response = await client.get("/prices")

    assert response.status_code == 422


async def test_get_latest_price_returns_not_found_when_ticker_has_no_prices(
    api_client: tuple[httpx.AsyncClient, MagicMock],
) -> None:
    client, repository = api_client
    repository.get_latest.return_value = None

    response = await client.get("/prices/latest", params={"ticker": "btc"})

    assert response.status_code == 404


async def test_get_prices_by_date_passes_utc_date_to_repository(
    api_client: tuple[httpx.AsyncClient, MagicMock],
) -> None:
    client, repository = api_client
    repository.get_all_for_date.return_value = [
        TickerPrice(ticker=Ticker.BTC.value, price=65000.12, timestamp=1735689600)
    ]

    response = await client.get("/prices/by-date", params={"ticker": "btc", "date": "2025-01-01"})

    assert response.status_code == 200
    assert response.json() == [{"ticker": "btc", "price": 65000.12, "timestamp": 1735689600}]
    repository.get_all_for_date.assert_awaited_once_with(Ticker.BTC, dt.date(2025, 1, 1))
