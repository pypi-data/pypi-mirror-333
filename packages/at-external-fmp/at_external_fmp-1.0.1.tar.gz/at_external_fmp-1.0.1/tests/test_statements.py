import pytest
from at_external_fmp.statements import *

@pytest.mark.asyncio
async def test_income_statement():
    result = await income_statement("AAPL", period="Q3", limit=10)
    assert result is not None and len(result) == 10

@pytest.mark.asyncio
async def test_income_statement_growth():
    result = await income_statement_growth("AAPL", period="QUARTER", limit=10)
    assert result is not None and len(result) == 10

@pytest.mark.asyncio
async def test_balance_sheet_statement():
    result = await balance_sheet_statement("AAPL", period="FY", limit=10)
    assert result is not None and len(result) == 10

@pytest.mark.asyncio
async def test_balance_sheet_statement_growth():
    result = await balance_sheet_statement_growth("AAPL", period="FY", limit=10)
    assert result is not None and len(result) == 10

@pytest.mark.asyncio
async def test_cash_flow_statement():
    result = await cash_flow_statement("AAPL", period="FY", limit=10)
    assert result is not None and len(result) == 10

@pytest.mark.asyncio
async def test_cash_flow_statement_growth():
    result = await cash_flow_statement_growth("AAPL", period="FY", limit=10)
    assert result is not None and len(result) == 10

@pytest.mark.asyncio
async def test_financial_growth():
    result = await financial_growth("AAPL", period="QUARTER", limit=5)
    assert result is not None and len(result) == 5

@pytest.mark.asyncio
async def test_key_metrics():
    result = await key_metrics("AAPL", limit=10)
    assert result is not None and len(result) == 10

@pytest.mark.asyncio
async def test_key_metrics_ttm():
    result = await key_metrics_ttm("AAPL")
    assert result is not None and len(result) == 1

@pytest.mark.asyncio
async def test_ratios():
    result = await ratios("AAPL", limit=10)
    assert result is not None and len(result) == 10

@pytest.mark.asyncio
async def test_ratios_ttm():
    result = await ratios_ttm("AAPL")
    assert result is not None and len(result) == 1

@pytest.mark.asyncio
async def test_financial_scores():
    result = await financial_scores("AAPL")
    assert result is not None and len(result) == 1

@pytest.mark.asyncio
async def test_owner_earnings():
    result = await owner_earnings("AAPL", limit=10)
    assert result is not None and len(result) == 10
    
@pytest.mark.asyncio
async def test_enterprise_values():
    result = await enterprise_values("AAPL", period="annual", limit=10)
    assert result is not None and len(result) == 10
