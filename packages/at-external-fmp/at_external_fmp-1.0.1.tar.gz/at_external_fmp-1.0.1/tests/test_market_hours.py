import pytest
from at_external_fmp.market_hours import *

@pytest.mark.asyncio
async def test_exchange_market_hours():
    result = await exchange_market_hours("NASDAQ")
    assert result is not None and len(result) == 1

@pytest.mark.asyncio
async def test_all_exchange_market_hours():
    result = await all_exchange_market_hours()
    assert result is not None and len(result) > 0