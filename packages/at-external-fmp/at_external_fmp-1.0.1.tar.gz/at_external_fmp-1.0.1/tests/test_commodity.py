import pytest
from at_external_fmp.commodity import *

@pytest.mark.asyncio
async def test_commodities_list():
    result = await commodities_list()
    assert result is not None and len(result) > 0