from typing import List
from ._client import Client
from .schema.forex import ForexItem

async def forex_list() -> List[ForexItem]:
    """
    Get forex list.
    """
    async with Client() as client:
        return [ForexItem(**item) for item in await client.get("forex-list")]