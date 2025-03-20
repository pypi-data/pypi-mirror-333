from typing import List
from ._client import Client
from .schema.market_hours import MarketHours

async def exchange_market_hours(exchange: str) -> List[MarketHours]:
    """
    Get the exchange market hours.
    """
    params = {
        "exchange": exchange
    }
    async with Client() as client:
        return [MarketHours(**item) for item in await client.get("exchange-market-hours", params)]

async def all_exchange_market_hours() -> List[MarketHours]:
    """
    Get all exchange market hours.
    """
    async with Client() as client:
        return [MarketHours(**item) for item in await client.get("all-exchange-market-hours")]