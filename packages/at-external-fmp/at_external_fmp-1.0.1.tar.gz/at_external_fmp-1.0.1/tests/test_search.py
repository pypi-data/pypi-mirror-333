import pytest
from at_external_fmp.search import *

@pytest.mark.asyncio
async def test_search_symbol():
    result = await search_symbol("AAPL")
    assert result is not None and len(result) > 0

async def test_search_name():
    result = await search_name("Apple Inc.")
    assert result is not None and len(result) > 0

async def test_search_cik():
    result = await search_cik("320193")
    assert result is not None and len(result) > 0

async def test_search_cusip():
    result = await search_cusip("037833100")
    assert result is not None and len(result) > 0

async def test_search_isin():
    result = await search_isin("US0378331005")
    assert result is not None and len(result) > 0