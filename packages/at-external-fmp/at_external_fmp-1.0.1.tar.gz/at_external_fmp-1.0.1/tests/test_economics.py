import pytest
from at_external_fmp.economics import *

@pytest.mark.asyncio
async def test_treasury_rates():
    result = await treasury_rates(from_date="2025-03-01", to_date="2025-03-31")
    assert result is not None and len(result) > 0

@pytest.mark.asyncio
async def test_economic_indicators():
    result = await economic_indicators("GDP")
    assert result is not None and len(result) > 0

@pytest.mark.asyncio
async def test_economic_calendar():
    result = await economic_calendar()
    assert result is not None and len(result) > 0

@pytest.mark.asyncio
async def test_market_risk_premium():
    result = await market_risk_premium()
    assert result is not None and len(result) > 0