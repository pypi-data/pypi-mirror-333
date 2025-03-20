import pytest
from at_external_fmp.market_performance import *
from datetime import datetime, timedelta

def _get_latest_trading_date() -> str:
    """
    Get the latest trading day.
    """
    today = datetime.now()
    # 5 = Saturday, 6 = Sunday in weekday() (0 is Monday)
    if today.weekday() == 5:  # Saturday
        return (today - timedelta(days=1)).strftime("%Y-%m-%d")  # Return Friday
    elif today.weekday() == 6:  # Sunday
        return (today - timedelta(days=2)).strftime("%Y-%m-%d")  # Return Friday
    else:
        return today.strftime("%Y-%m-%d")  # Return today for weekdays

@pytest.mark.asyncio
async def test_sector_performance_snapshot():
    date = _get_latest_trading_date()
    result = await sector_performance_snapshot(date, "NASDAQ")
    assert result is not None and len(result) > 0

@pytest.mark.asyncio
async def test_sector_pe_snapshot():
    date = _get_latest_trading_date()
    result = await sector_pe_snapshot(date, "NASDAQ")
    assert result is not None and len(result) > 0

@pytest.mark.asyncio
async def test_historical_sector_performance():
    to_date = datetime.now()
    from_date = to_date - timedelta(days=14)
    result = await historical_sector_performance("Energy", "AMEX", from_date.strftime("%Y-%m-%d"), to_date.strftime("%Y-%m-%d"))
    assert result is not None and len(result) > 0 and len(result) <= 14

@pytest.mark.asyncio
async def test_historical_sector_pe():
    to_date = datetime.now()
    from_date = to_date - timedelta(days=14)
    result = await historical_sector_pe("Energy", "AMEX", from_date.strftime("%Y-%m-%d"), to_date.strftime("%Y-%m-%d"))
    assert result is not None and len(result) > 0 and len(result) <= 14

@pytest.mark.asyncio
async def test_industry_performance_snapshot():
    date = _get_latest_trading_date()
    result = await industry_performance_snapshot(date, "NASDAQ")
    assert result is not None and len(result) > 0

@pytest.mark.asyncio
async def test_industry_pe_snapshot():
    date = _get_latest_trading_date()
    result = await industry_pe_snapshot(date, "NASDAQ")
    assert result is not None and len(result) > 0

@pytest.mark.asyncio
async def test_historical_industry_performance():
    to_date = datetime.now()
    from_date = to_date - timedelta(days=14)
    result = await historical_industry_performance("Biotechnology", "NASDAQ", from_date.strftime("%Y-%m-%d"), to_date.strftime("%Y-%m-%d"))
    assert result is not None and len(result) > 0 and len(result) <= 14

@pytest.mark.asyncio
async def test_historical_industry_pe():
    to_date = datetime.now()
    from_date = to_date - timedelta(days=14)
    result = await historical_industry_pe("Biotechnology", "NASDAQ", from_date.strftime("%Y-%m-%d"), to_date.strftime("%Y-%m-%d"))
    assert result is not None and len(result) > 0 and len(result) <= 14

@pytest.mark.asyncio
async def test_biggest_gainers():
    result = await biggest_gainers()
    assert result is not None and len(result) > 0

@pytest.mark.asyncio
async def test_biggest_losers():
    result = await biggest_losers()
    assert result is not None and len(result) > 0

@pytest.mark.asyncio
async def test_most_actives():
    result = await most_actives()
    assert result is not None and len(result) > 0