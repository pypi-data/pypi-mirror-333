from typing import List, Optional
from ._client import Client
from .schema.market_performance import SectorPerformanceSnapshot, IndustryPerformanceSnapshot, SectorPESnapshot, IndustryPESnapshot, Stock

async def sector_performance_snapshot(date: str, exchange: str) -> List[SectorPerformanceSnapshot]:
    """
    Get the sector performance snapshot.
    """
    params = {
        "date": date,
        "exchange": exchange
    }
    async with Client() as client:
        return [SectorPerformanceSnapshot(**item) for item in await client.get("sector-performance-snapshot", params)]

async def sector_pe_snapshot(date: str, exchange: str) -> List[SectorPESnapshot]:
    """
    Get the sector PE snapshot.
    """
    params = {
        "date": date,
        "exchange": exchange
    }
    async with Client() as client:
        return [SectorPESnapshot(**item) for item in await client.get("sector-pe-snapshot", params)]

async def historical_sector_performance(sector: str, exchange: str, from_date: Optional[str] = None, to_date: Optional[str] = None) -> List[SectorPerformanceSnapshot]:
    """
    Get the historical sector performance.
    """
    params = {
        "sector": sector,
        "exchange": exchange,
    }
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date
    async with Client() as client:
        return [SectorPerformanceSnapshot(**item) for item in await client.get("historical-sector-performance", params)]

async def historical_sector_pe(sector: str, exchange: str, from_date: Optional[str] = None, to_date: Optional[str] = None) -> List[SectorPESnapshot]:
    """
    Get the historical sector PE.
    """
    params = {
        "sector": sector,
        "exchange": exchange,
    }
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date
    async with Client() as client:
        return [SectorPESnapshot(**item) for item in await client.get("historical-sector-pe", params)]

async def industry_performance_snapshot(date: str, exchange: str) -> List[IndustryPerformanceSnapshot]:
    """
    Get the industry performance snapshot.
    """
    params = {
        "date": date,
        "exchange": exchange
    }
    async with Client() as client:
        return [IndustryPerformanceSnapshot(**item) for item in await client.get("industry-performance-snapshot", params)]

async def industry_pe_snapshot(date: str, exchange: str) -> List[IndustryPESnapshot]:
    """
    Get the industry PE snapshot.
    """
    params = {
        "date": date,
        "exchange": exchange
    }
    async with Client() as client:
        return [IndustryPESnapshot(**item) for item in await client.get("industry-pe-snapshot", params)]

async def historical_industry_performance(industry: str, exchange: str, from_date: Optional[str] = None, to_date: Optional[str] = None) -> List[IndustryPerformanceSnapshot]:
    """
    Get the historical industry performance.
    """
    params = {
        "industry": industry,
        "exchange": exchange,
    }
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date
    async with Client() as client:
        return [IndustryPerformanceSnapshot(**item) for item in await client.get("historical-industry-performance", params)]

async def historical_industry_pe(industry: str, exchange: str, from_date: Optional[str] = None, to_date: Optional[str] = None) -> List[IndustryPESnapshot]:
    """
    Get the historical industry PE.
    """
    params = {
        "industry": industry,
        "exchange": exchange,
    }
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date
    async with Client() as client:
        return [IndustryPESnapshot(**item) for item in await client.get("historical-industry-pe", params)]

async def biggest_gainers() -> List[Stock]:
    """
    Get the biggest gainers.
    """
    async with Client() as client:
        return [Stock(**item) for item in await client.get("biggest-gainers")]

async def biggest_losers() -> List[Stock]:
    """
    Get the biggest losers.
    """
    async with Client() as client:
        return [Stock(**item) for item in await client.get("biggest-losers")]

async def most_actives() -> List[Stock]:
    """
    Get the most actives.
    """
    async with Client() as client:
        return [Stock(**item) for item in await client.get("most-actives")]