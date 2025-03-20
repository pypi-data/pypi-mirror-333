from typing import List
from ._client import Client
from .schema.index import IndexItem, IndexConstituent

async def index_list() -> List[IndexItem]:
    """
    Get a list of all indices.
    """
    async with Client() as client:
        return [IndexItem(**item) for item in await client.get("index-list")]

async def sp500_constituent() -> List[IndexConstituent]:
    """
    Get the constituents of the S&P 500.
    """
    async with Client() as client:
        return [IndexConstituent(**item) for item in await client.get("sp500-constituent")]

async def nasdaq_constituent() -> List[IndexConstituent]:
    """
    Get the constituents of the NASDAQ.
    """
    async with Client() as client:
        return [IndexConstituent(**item) for item in await client.get("nasdaq-constituent")]

async def dowjones_constituent() -> List[IndexConstituent]:
    """
    Get the constituents of the Dow Jones.
    """
    async with Client() as client:
        return [IndexConstituent(**item) for item in await client.get("dowjones-constituent")]

