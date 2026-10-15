import collections.abc as cabc
import datetime as dt
import typing as tp

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from deribit_price_api.domain.price import Price
from deribit_price_api.domain.ticker import Ticker
from deribit_price_api.infrastructure.models import TickerPrice


class PriceRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add_many(self, prices: cabc.Iterable[Price]) -> None:
        self._session.add_all(
            TickerPrice(ticker=price.ticker.value, price=price.value, timestamp=price.timestamp)
            for price in prices
        )
        await self._session.commit()

    async def get_all_for_ticker(self, ticker: Ticker) -> list[TickerPrice]:
        query = (
            select(TickerPrice)
            .where(TickerPrice.ticker == ticker.value)
            .order_by(TickerPrice.timestamp)
        )
        result = await self._session.scalars(query)
        prices = tp.cast(list[TickerPrice], result.all())
        return prices

    async def get_latest(self, ticker: Ticker) -> TickerPrice | None:
        query = (
            select(TickerPrice)
            .where(TickerPrice.ticker == ticker.value)
            .order_by(TickerPrice.timestamp.desc())
            .limit(1)
        )
        result = await self._session.scalar(query)
        return result

    async def get_all_for_date(self, ticker: Ticker, requested_date: dt.date) -> list[TickerPrice]:
        start_datetime = dt.datetime.combine(requested_date, dt.time.min, tzinfo=dt.UTC)
        end_datetime = start_datetime + dt.timedelta(days=1)
        start = int(start_datetime.timestamp())
        end = int(end_datetime.timestamp())
        query = (
            select(TickerPrice)
            .where(
                TickerPrice.ticker == ticker.value,
                TickerPrice.timestamp >= start,
                TickerPrice.timestamp < end,
            )
            .order_by(TickerPrice.timestamp)
        )
        result = await self._session.scalars(query)
        prices = tp.cast(list[TickerPrice], result.all())
        return prices
