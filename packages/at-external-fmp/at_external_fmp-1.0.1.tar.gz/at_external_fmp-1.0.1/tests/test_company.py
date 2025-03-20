import pytest
from at_external_fmp.company import *

@pytest.mark.asyncio
async def test_profile():
    result = await profile("AAPL")
    assert result is not None and len(result) == 1

@pytest.mark.asyncio
async def test_profile_cik():
    result = await profile_cik("320193")
    assert result is not None and len(result) == 1

@pytest.mark.asyncio
async def test_company_notes():
    result = await company_notes("AAPL")
    assert result is not None and len(result) > 0

@pytest.mark.asyncio
async def test_stock_peers():
    result = await stock_peers("AAPL")
    assert result is not None and len(result) > 0

@pytest.mark.asyncio
async def test_delisted_companies():
    result = await delisted_companies(page=0, limit=10)
    assert result is not None and len(result) == 10

@pytest.mark.asyncio
async def test_employee_count():
    result = await employee_count("AAPL", limit=10)
    assert result is not None and len(result) <= 10

@pytest.mark.asyncio
async def test_historical_employee_count():
    result = await historical_employee_count("AAPL", page=0, limit=10)
    assert result is not None and len(result) <= 10

@pytest.mark.asyncio
async def test_market_capitalization():
    result = await market_capitalization("AAPL")
    assert result is not None and len(result) == 1

@pytest.mark.asyncio
async def test_market_capitalization_batch():
    result = await market_capitalization_batch(["AAPL", "TSLA"])
    assert result is not None and len(result) == 2

@pytest.mark.asyncio
async def test_historical_market_capitalization():
    result = await historical_market_capitalization("AAPL", from_date="2024-12-01", to_date="2024-12-31")
    assert result is not None and len(result) > 10

@pytest.mark.asyncio
async def test_shares_float():
    result = await shares_float("AAPL")
    assert result is not None and len(result) == 1

@pytest.mark.asyncio
async def test_shares_float_all():
    result = await shares_float_all()
    assert result is not None and len(result) > 0

@pytest.mark.asyncio
async def test_mergers_acquisitions_latest():
    result = await mergers_acquisitions_latest(page=0, limit=10)
    assert result is not None and len(result) == 10

@pytest.mark.asyncio
async def test_mergers_acquisitions_search():
    result = await mergers_acquisitions_search("Apple")
    assert result is not None and len(result) > 0

@pytest.mark.asyncio
async def test_key_executives():
    result = await key_executives("AAPL", active=True)
    assert result is not None and len(result) > 0

@pytest.mark.asyncio
async def test_governance_executive_compensation():
    result = await governance_executive_compensation("AAPL")
    assert result is not None and len(result) > 0
    
@pytest.mark.asyncio
async def test_executive_compensation_benchmark():
    result = await executive_compensation_benchmark()
    assert result is not None and len(result) > 0