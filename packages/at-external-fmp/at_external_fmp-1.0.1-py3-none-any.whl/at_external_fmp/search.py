from typing import List, Dict, Any, Optional
from ._client import Client
from .schema.search import SearchResult, SearchCIKResult, SearchCusipResult, SearchISINResult

async def search_symbol(query: str, limit: Optional[int] = None, exchange: Optional[str] = None) -> List[SearchResult]:
    """
    Search for symbols based on a query.
    """
    params = {"query": query}
    if limit:
        params["limit"] = limit
    if exchange:
        params["exchange"] = exchange
    async with Client() as client:
        return [SearchResult(**item) for item in await client.get("search-symbol", params)]

async def search_name(query: str, limit: Optional[int] = None, exchange: Optional[str] = None) -> List[SearchResult]:
    """
    Search for symbols based on a name.
    """
    params = {"query": query}
    if limit:
        params["limit"] = limit
    if exchange:
        params["exchange"] = exchange
    
    async with Client() as client:
        return [SearchResult(**item) for item in await client.get("search-name", params)]

async def search_cik(cik: str, limit: Optional[int] = None) -> List[SearchCIKResult]:
    """
    Search for symbols based on a CIK.
    """
    params = {"cik": cik}
    if limit:
        params["limit"] = limit
    
    async with Client() as client:
        return [SearchCIKResult(**item) for item in await client.get("search-cik", params)]

async def search_cusip(cusip: str) -> List[SearchCusipResult]:
    """
    Search for symbols based on a CUSIP.
    """
    params = {"cusip": cusip}
    async with Client() as client:
        return [SearchCusipResult(**item) for item in await client.get("search-cusip", params)]

async def search_isin(isin: str) -> List[SearchISINResult]:
    """
    Search for symbols based on a ISIN.
    """
    params = {"isin": isin}
    async with Client() as client:
        return [SearchISINResult(**item) for item in await client.get("search-isin", params)]