import pytest
from at_external_fmp.chart import *

@pytest.mark.asyncio
async def test_historical_price_eod_light():
    result = await historical_price_eod_light("AAPL", "2025-01-01", "2025-01-31")
    assert result is not None and len(result) > 0

@pytest.mark.asyncio
async def test_historical_price_eod_full():
    result = await historical_price_eod_full("AAPL", "2025-01-01", "2025-01-31")
    assert result is not None and len(result) > 0

@pytest.mark.asyncio
async def test_historical_price_eod_non_split_adjusted():
    result = await historical_price_eod_non_split_adjusted("AAPL", "2025-01-01", "2025-01-31")
    assert result is not None and len(result) > 0

@pytest.mark.asyncio
async def test_historical_price_eod_dividend_adjusted():
    result = await historical_price_eod_dividend_adjusted("AAPL", "2025-01-01", "2025-01-31")
    assert result is not None and len(result) > 0

@pytest.mark.asyncio
async def test_historical_chart_5min():
    result = await historical_chart_5min("AAPL", "2025-03-07", "2025-03-07")
    assert result is not None and len(result) > 0

@pytest.mark.asyncio
async def test_historical_chart_15min():
    result = await historical_chart_15min("AAPL", "2025-03-07", "2025-03-07")
    assert result is not None and len(result) > 0

@pytest.mark.asyncio
async def test_historical_chart_30min():
    result = await historical_chart_30min("AAPL", "2025-03-07", "2025-03-07")
    assert result is not None and len(result) > 0

@pytest.mark.asyncio
async def test_historical_chart_1hr():
    result = await historical_chart_1hr("AAPL", "2025-03-07", "2025-03-07")
    assert result is not None and len(result) > 0

@pytest.mark.asyncio
async def test_historical_chart_4hr():
    result = await historical_chart_4hr("AAPL", "2025-03-07", "2025-03-07")
    assert result is not None and len(result) > 0