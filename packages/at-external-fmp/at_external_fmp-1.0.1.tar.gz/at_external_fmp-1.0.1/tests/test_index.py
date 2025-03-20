import pytest
from at_external_fmp.index import *

@pytest.mark.asyncio
async def test_index_list():
    result = await index_list()
    assert result is not None and len(result) > 0

@pytest.mark.asyncio
async def test_sp500_constituent():
    result = await sp500_constituent()
    assert result is not None and len(result) > 0

@pytest.mark.asyncio
async def test_nasdaq_constituent():
    result = await nasdaq_constituent()
    assert result is not None and len(result) > 0

@pytest.mark.asyncio
async def test_dowjones_constituent():
    result = await dowjones_constituent()
    assert result is not None and len(result) > 0