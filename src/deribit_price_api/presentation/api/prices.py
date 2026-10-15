import datetime as dt

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from deribit_price_api.domain.ticker import Ticker
from deribit_price_api.infrastructure.models import TickerPrice
from deribit_price_api.infrastructure.repositories.prices import PriceRepository
from deribit_price_api.presentation.dependencies import get_session
from deribit_price_api.presentation.schemas import PriceRead

router = APIRouter(prefix="/prices", tags=["prices"])


def get_repository(session: AsyncSession = Depends(get_session)) -> PriceRepository:
    return PriceRepository(session)


@router.get("", response_model=list[PriceRead])
async def get_prices(ticker: Ticker, repository: PriceRepository = Depends(get_repository)) -> list[TickerPrice]:
    prices = await repository.get_all_for_ticker(ticker)
    return prices


@router.get("/latest", response_model=PriceRead)
async def get_latest_price(ticker: Ticker, repository: PriceRepository = Depends(get_repository)) -> TickerPrice:
    result = await repository.get_latest(ticker)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No prices found for ticker")
    return result


@router.get("/by-date", response_model=list[PriceRead])
async def get_prices_by_date(
    ticker: Ticker,
    price_date: dt.date = Query(..., alias="date", description="UTC date in YYYY-MM-DD format"),
    repository: PriceRepository = Depends(get_repository),
) -> list[TickerPrice]:
    prices = await repository.get_all_for_date(ticker, price_date)
    return prices
