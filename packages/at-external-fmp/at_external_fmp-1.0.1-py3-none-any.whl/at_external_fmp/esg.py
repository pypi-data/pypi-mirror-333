from typing import List
from ._client import Client
from .schema.esg import (
    ESGDisclosureItem,
    ESGRatingItem,
    ESGBenchmarkItem
)

async def esg_disclosures(symbol: str) -> List[ESGDisclosureItem]:
    """
    Get ESG disclosures for a symbol.
    """
    params = {"symbol": symbol}
    async with Client() as client:
        return [ESGDisclosureItem(**item) for item in await client.get("esg-disclosures", params)]

async def esg_ratings(symbol: str) -> List[ESGRatingItem]:
    """
    Get ESG ratings for a symbol.
    """
    params = {"symbol": symbol}
    async with Client() as client:
        return [ESGRatingItem(**item) for item in await client.get("esg-ratings", params)]

async def esg_benchmark() -> List[ESGBenchmarkItem]:
    """
    Get ESG benchmark.
    """
    async with Client() as client:
        return [ESGBenchmarkItem(**item) for item in await client.get("esg-benchmark")]