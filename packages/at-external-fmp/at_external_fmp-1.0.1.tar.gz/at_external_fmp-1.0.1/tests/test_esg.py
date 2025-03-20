import pytest
from at_external_fmp.esg import *

@pytest.mark.asyncio
async def test_esg_disclosures():
    result = await esg_disclosures("AAPL")
    assert result is not None and len(result) > 0

@pytest.mark.asyncio
async def test_esg_ratings():
    result = await esg_ratings("AAPL")
    assert result is not None and len(result) > 0

@pytest.mark.asyncio
async def test_esg_benchmark():
    result = await esg_benchmark()
    assert result is not None and len(result) > 0