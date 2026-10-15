import datetime as dt

from deribit_price_api.domain.ticker import Ticker
from deribit_price_api.infrastructure.models import TickerPrice
from deribit_price_api.infrastructure.repositories.prices import PriceRepository


def create_ticker_price(ticker: Ticker, value: float, timestamp: int) -> TickerPrice:
    return TickerPrice(ticker=ticker.value, price=value, timestamp=timestamp)


async def test_returns_prices_only_for_requested_ticker(mocked_session):
    expected = [create_ticker_price(Ticker.BTC, 65000.12, 1_704_067_200)]
    mocked_session.scalars.return_value.all.return_value = expected
    repository = PriceRepository(mocked_session)

    result = await repository.get_all_for_ticker(Ticker.BTC)

    assert result == expected
    mocked_session.scalars.assert_called_once()


async def test_returns_newest_price(mocked_session):
    expected = create_ticker_price(Ticker.BTC, 65000.0, 1_704_067_260)
    mocked_session.scalar.return_value = expected
    repository = PriceRepository(mocked_session)

    assert await repository.get_latest(Ticker.BTC) == expected
    mocked_session.scalar.assert_called_once()


async def test_filters_prices_by_utc_date(mocked_session):
    expected = [create_ticker_price(Ticker.BTC, 1.0, 1_704_067_200)]
    mocked_session.scalars.return_value.all.return_value = expected
    repository = PriceRepository(mocked_session)

    result = await repository.get_all_for_date(Ticker.BTC, dt.date(2024, 1, 1))

    assert result == expected
    statement = mocked_session.scalars.call_args.args[0]
    assert statement.compile().params == {
        "ticker_1": "btc",
        "timestamp_1": 1_704_067_200,
        "timestamp_2": 1_704_153_600,
    }
