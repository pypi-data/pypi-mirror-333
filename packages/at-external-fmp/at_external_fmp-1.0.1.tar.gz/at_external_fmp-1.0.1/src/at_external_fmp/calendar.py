from typing import List, Optional
from ._client import Client
from .schema.calendar import (
    Dividends, Earnings, Splits, IPOs, IPOsDisclosure, IPOsProspectus
)

async def dividends(symbol: str, limit: Optional[int] = None) -> List[Dividends]:
    """
    Get dividends for a symbol.
    """
    params = {"symbol": symbol}
    if limit:
        params["limit"] = limit
    async with Client() as client:
        return [Dividends(**item) for item in await client.get("dividends", params)]

async def dividends_calendar(from_date: Optional[str] = None, to_date: Optional[str] = None) -> List[Dividends]:
    """
    Get dividends calendar.
    """
    params = {}
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date
    async with Client() as client:
        return [Dividends(**item) for item in await client.get("dividends-calendar", params)]

async def earnings(symbol: str, limit: Optional[int] = None) -> List[Earnings]:
    """
    Get earnings for a symbol.
    """
    params = {"symbol": symbol}
    if limit:
        params["limit"] = limit
    async with Client() as client:
        return [Earnings(**item) for item in await client.get("earnings", params)]

async def earnings_calendar(from_date: Optional[str] = None, to_date: Optional[str] = None) -> List[Earnings]:
    """
    Get earnings calendar.
    """
    params = {}
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date
    async with Client() as client:
        return [Earnings(**item) for item in await client.get("earnings-calendar", params)]

async def splits(symbol: str, limit: Optional[int] = None) -> List[Splits]:
    """
    Get splits for a symbol.
    """
    params = {"symbol": symbol}
    if limit:
        params["limit"] = limit
    async with Client() as client:
        return [Splits(**item) for item in await client.get("splits", params)]

async def splits_calendar(from_date: Optional[str] = None, to_date: Optional[str] = None) -> List[Splits]:
    """
    Get splits calendar.
    """
    params = {}
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date
    async with Client() as client:
        return [Splits(**item) for item in await client.get("splits-calendar", params)]

async def ipos_calendar(from_date: Optional[str] = None, to_date: Optional[str] = None) -> List[IPOs]:
    """
    Get IPO calendar.
    """
    params = {}
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date
    async with Client() as client:
        return [IPOs(**item) for item in await client.get("ipos-calendar", params)]

async def ipos_disclosure(from_date: Optional[str] = None, to_date: Optional[str] = None) -> List[IPOsDisclosure]:
    """
    Get IPO disclosure.
    """
    params = {}
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date
    async with Client() as client:
        return [IPOsDisclosure(**item) for item in await client.get("ipos-disclosure", params)]

async def ipos_prospectus(from_date: Optional[str] = None, to_date: Optional[str] = None, page: Optional[int] = None, limit: Optional[int] = None) -> List[IPOsProspectus]:
    """
    Get IPO prospectus.
    """
    params = {}
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date
    if page:
        params["page"] = page
    if limit:
        params["limit"] = limit
    async with Client() as client:
        return [IPOsProspectus(**item) for item in await client.get("ipos-prospectus", params)]