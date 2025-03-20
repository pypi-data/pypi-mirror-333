from typing import List, Dict, Any
from ._client import Client
from .schema.etf_and_mutual_funds import *

async def etf_holdings(symbol: str) -> List[ETFHolding]:
    """
    Get ETF holdings.
    """
    params = {"symbol": symbol}
    async with Client() as client:
        return [ETFHolding(**item) for item in await client.get("etf/holdings", params)]

async def etf_info(symbol: str) -> List[ETFInfo]:
    """
    Get ETF info.
    """
    params = {"symbol": symbol}
    async with Client() as client:
        return [ETFInfo(**item) for item in await client.get("etf/info", params)]

async def etf_country_weightings(symbol: str) -> List[ETFCountryWeight]:
    """
    Get ETF country weightings.
    """
    params = {"symbol": symbol}
    async with Client() as client:
        return [ETFCountryWeight(**item) for item in await client.get("etf/country-weightings", params)]

async def etf_asset_exposure(symbol: str) -> List[ETFAssetExposure]:
    """
    Get ETF asset exposure.
    """
    params = {"symbol": symbol}
    async with Client() as client:
        return [ETFAssetExposure(**item) for item in await client.get("etf/asset-exposure", params)]

async def etf_sector_weightings(symbol: str) -> List[ETFSectorWeight]:
    """
    Get ETF sector weightings.
    """
    params = {"symbol": symbol}
    async with Client() as client:
        return [ETFSectorWeight(**item) for item in await client.get("etf/sector-weightings", params)]