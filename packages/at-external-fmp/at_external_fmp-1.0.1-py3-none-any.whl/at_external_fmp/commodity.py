from typing import List
from ._client import Client
from .schema.commodity import CommodityItem

async def commodities_list() -> List[CommodityItem]:
    """
    Get commodities list.
    """
    async with Client() as client:
        return [CommodityItem(**commodity) for commodity in await client.get("commodities-list")]