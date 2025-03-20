from typing import List
from ._client import Client
from .schema.crypto import CryptoCurrency

async def cryptocurrency_list() -> List[CryptoCurrency]:
    """
    Get cryptocurrency list.
    """
    async with Client() as client:
        return [CryptoCurrency(**crypto) for crypto in await client.get("cryptocurrency-list")]