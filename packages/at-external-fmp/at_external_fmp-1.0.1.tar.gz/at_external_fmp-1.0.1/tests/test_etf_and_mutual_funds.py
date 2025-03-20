import pytest
from at_external_fmp.etf_and_mutual_funds import *

@pytest.mark.asyncio
async def test_etf_holdings():
    result = await etf_holdings("SPY")
    assert result is not None and len(result) > 0

@pytest.mark.asyncio
async def test_etf_info():
    result = await etf_info("SPY")
    assert result is not None and len(result) == 1

@pytest.mark.asyncio
async def test_etf_country_weightings():
    result = await etf_country_weightings("SPY")
    assert result is not None and len(result) > 0

@pytest.mark.asyncio
async def test_etf_asset_exposure():
    result = await etf_asset_exposure("SPY")
    assert result is not None and len(result) > 0

@pytest.mark.asyncio
async def test_etf_sector_weightings():
    result = await etf_sector_weightings("SPY")
    assert result is not None and len(result) > 0