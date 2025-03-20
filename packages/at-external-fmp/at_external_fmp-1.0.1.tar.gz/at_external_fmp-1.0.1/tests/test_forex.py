import pytest
from at_external_fmp.forex import *

@pytest.mark.asyncio
async def test_forex_list():
    result = await forex_list()
    assert result is not None and len(result) > 0