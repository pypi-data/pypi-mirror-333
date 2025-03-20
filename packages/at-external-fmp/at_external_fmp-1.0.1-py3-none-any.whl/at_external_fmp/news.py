from typing import List, Optional
from ._client import Client
from .schema.news import NewsItem, FMPArticle

async def fmp_articles() -> List[FMPArticle]:
    """
    Get FMP articles.
    """
    async with Client() as client:
        return [FMPArticle(**item) for item in await client.get("fmp-articles")]

async def news_general_latest(from_date: Optional[str] = None, to_date: Optional[str] = None, page: Optional[int] = None, limit: Optional[int] = None) -> List[NewsItem]:
    """
    Get general latest news.
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
        return [NewsItem(**item) for item in await client.get("news/general-latest", params)]

async def news_stock_latest(from_date: Optional[str] = None, to_date: Optional[str] = None, page: Optional[int] = None, limit: Optional[int] = None) -> List[NewsItem]:
    """
    Get stock latest news.
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
        return [NewsItem(**item) for item in await client.get("news/stock-latest", params)]

async def news_crypto_latest(from_date: Optional[str] = None, to_date: Optional[str] = None, page: Optional[int] = None, limit: Optional[int] = None) -> List[NewsItem]:
    """
    Get crypto latest news.
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
        return [NewsItem(**item) for item in await client.get("news/crypto-latest", params)]

async def news_forex_latest(from_date: Optional[str] = None, to_date: Optional[str] = None, page: Optional[int] = None, limit: Optional[int] = None) -> List[NewsItem]:
    """
    Get forex latest news.
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
        return [NewsItem(**item) for item in await client.get("news/forex-latest", params)]

async def news_stock(symbols: List[str], from_date: Optional[str] = None, to_date: Optional[str] = None, page: Optional[int] = None, limit: Optional[int] = None) -> List[NewsItem]:
    """
    Get news for a list of stocks.
    """
    params = {}
    if symbols:
        params["symbols"] = ",".join(symbols)
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date
    if page:
        params["page"] = page
    if limit:
        params["limit"] = limit
    async with Client() as client:
        return [NewsItem(**item) for item in await client.get("news/stock", params)]

async def news_crypto(symbols: List[str], from_date: Optional[str] = None, to_date: Optional[str] = None, page: Optional[int] = None, limit: Optional[int] = None) -> List[NewsItem]:
    """
    Get news for a list of cryptocurrencies.
    """
    params = {}
    if symbols:
        params["symbols"] = ",".join(symbols)
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date
    if page:
        params["page"] = page
    if limit:
        params["limit"] = limit
    async with Client() as client:
        return [NewsItem(**item) for item in await client.get("news/crypto", params)]

async def news_forex(symbols: List[str], from_date: Optional[str] = None, to_date: Optional[str] = None, page: Optional[int] = None, limit: Optional[int] = None) -> List[NewsItem]:
    """
    Get news for a list of forex.
    """
    params = {}
    if symbols:
        params["symbols"] = ",".join(symbols)
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date
    if page:
        params["page"] = page
    if limit:
        params["limit"] = limit
    async with Client() as client:
        return [NewsItem(**item) for item in await client.get("news/forex", params)]