from typing import List, Optional
from ._client import Client
from .schema.economics import (
    TreasuryRate,
    EconomicIndicator,
    EconomicCalendarItem,
    MarketRiskPremiumItem
)


async def treasury_rates(from_date: Optional[str] = None, to_date: Optional[str] = None) -> List[TreasuryRate]:
    """
    Get treasury rates.
    """
    params = {}
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date
    async with Client() as client:
        return [TreasuryRate(**item) for item in await client.get("treasury-rates", params)]

async def economic_indicators(name: str) -> List[EconomicIndicator]:
    """
    Get economic indicators.
    """
    params = {"name": name}
    async with Client() as client:
        return [EconomicIndicator(**item) for item in await client.get("economic-indicators", params)]

async def economic_calendar(from_date: Optional[str] = None, to_date: Optional[str] = None) -> List[EconomicCalendarItem]:
    """
    Get economic calendar.
    """
    params = {}
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date
    async with Client() as client:
        return [EconomicCalendarItem(**item) for item in await client.get("economic-calendar", params)]

async def market_risk_premium() -> List[MarketRiskPremiumItem]:
    """
    Get market risk premium.
    """
    async with Client() as client:
        return [MarketRiskPremiumItem(**item) for item in await client.get("market-risk-premium")]