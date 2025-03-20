import pytest
from at_external_fmp.calendar import *

@pytest.mark.asyncio
async def test_dividends():
    result = await dividends("AAPL", limit=10)
    assert result is not None and len(result) == 10

@pytest.mark.asyncio
async def test_dividends_calendar():
    result = await dividends_calendar(from_date="2025-01-01", to_date="2025-12-31")
    assert result is not None and len(result) > 0

@pytest.mark.asyncio
async def test_earnings():
    result = await earnings("AAPL", limit=10)
    assert result is not None and len(result) == 10

@pytest.mark.asyncio
async def test_earnings_calendar():
    result = await earnings_calendar(from_date="2025-01-01", to_date="2025-12-31")
    assert result is not None and len(result) > 0

@pytest.mark.asyncio
async def test_splits():
    result = await splits("AAPL", limit=10)
    assert result is not None and len(result) <= 10

@pytest.mark.asyncio
async def test_splits_calendar():
    result = await splits_calendar(from_date="2025-01-01", to_date="2025-12-31")
    assert result is not None and len(result) > 0

@pytest.mark.asyncio
async def test_ipos_calendar():
    result = await ipos_calendar(from_date="2025-03-01", to_date="2025-05-31")
    assert result is not None and len(result) > 0

@pytest.mark.asyncio
async def test_ipos_disclosure():
    result = await ipos_disclosure(from_date="2025-03-01", to_date="2025-05-31")
    assert result is not None and len(result) > 0

@pytest.mark.asyncio
async def test_ipos_prospectus():
    result = await ipos_prospectus(from_date="2025-03-01", to_date="2025-05-31", page=0, limit=10)
    assert result is not None and len(result) == 10