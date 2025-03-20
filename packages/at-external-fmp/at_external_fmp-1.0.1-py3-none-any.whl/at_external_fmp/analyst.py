from typing import List, Optional
from ._client import Client
from .schema.analyst import (
    AnalystEstimates, RatingsSnapshot, RatingsHistorical, PriceTargetSummary, PriceTargetConsensus, 
    PriceTargetNews, Grades, GradesHistorical, GradesConsensus, GradesNews
)

async def analyst_estimates(symbol: str) -> List[AnalystEstimates]:
    """
    Get analyst estimates for a symbol.
    """
    params = {"symbol": symbol}
    async with Client() as client:
        return [AnalystEstimates(**item) for item in await client.get("analyst-estimates", params)]

async def ratings_snapshot(symbol: str) -> List[RatingsSnapshot]:
    """
    Get ratings snapshot for a symbol.
    """
    params = {"symbol": symbol}
    async with Client() as client:
        return [RatingsSnapshot(**item) for item in await client.get("ratings-snapshot", params)]

async def ratings_historical(symbol: str, limit: Optional[int] = None) -> List[RatingsHistorical]:
    """
    Get historical ratings for a symbol.
    """
    params = {"symbol": symbol}
    if limit:
        params["limit"] = limit
    async with Client() as client:
        return [RatingsHistorical(**item) for item in await client.get("ratings-historical", params)]

async def price_target_summary(symbol: str) -> List[PriceTargetSummary]:
    """
    Get price target summary for a symbol.
    """
    params = {"symbol": symbol}
    async with Client() as client:
        return [PriceTargetSummary(**item) for item in await client.get("price-target-summary", params)]

async def price_target_consensus(symbol: str) -> List[PriceTargetConsensus]:
    """
    Get price target consensus for a symbol.
    """
    params = {"symbol": symbol}
    async with Client() as client:
        return [PriceTargetConsensus(**item) for item in await client.get("price-target-consensus", params)]

async def price_target_news(symbol: str, limit: Optional[int] = None) -> List[PriceTargetNews]:
    """
    Get price target news for a symbol.
    """
    params = {"symbol": symbol}
    if limit:
        params["limit"] = limit
    async with Client() as client:
        return [PriceTargetNews(**item) for item in await client.get("price-target-news", params)]

async def price_target_latest_news(page: Optional[int] = None, limit: Optional[int] = None) -> List[PriceTargetNews]:
    """
    Get latest price target news.
    """
    params = {}
    if page:
        params["page"] = page
    if limit:
        params["limit"] = limit
    async with Client() as client:
        return [PriceTargetNews(**item) for item in await client.get("price-target-latest-news", params)]

async def grades(symbol: str) -> List[Grades]:
    """
    Get grades for a symbol.
    """
    params = {"symbol": symbol}
    async with Client() as client:
        return await client.get("grades", params)

async def grades_historical(symbol: str, limit: Optional[int] = None) -> List[GradesHistorical]:
    """
    Get historical grades for a symbol.
    """
    params = {"symbol": symbol}
    if limit:
        params["limit"] = limit
    async with Client() as client:
        return [GradesHistorical(**item) for item in await client.get("grades-historical", params)]

async def grades_consensus(symbol: str) -> List[GradesConsensus]:
    """
    Get consensus grades for a symbol.
    """
    params = {"symbol": symbol}
    async with Client() as client:
        return [GradesConsensus(**item) for item in await client.get("grades-consensus", params)]

async def grades_news(symbol: str, limit: Optional[int] = None) -> List[GradesNews]:
    """
    Get grades news for a symbol.
    """
    params = {"symbol": symbol}
    if limit:
        params["limit"] = limit
    async with Client() as client:
        return [GradesNews(**item) for item in await client.get("grades-news", params)]

async def grades_latest_news(page: Optional[int] = None, limit: Optional[int] = None) -> List[GradesNews]:
    """
    Get latest grades news.
    """
    params = {} 
    if page:
        params["page"] = page
    if limit:
        params["limit"] = limit
    async with Client() as client:
        return [GradesNews(**item) for item in await client.get("grades-latest-news", params)]
