import pytest
from at_external_fmp.directory import *

@pytest.mark.asyncio
async def test_stock_list():
    result = await stock_list()
    assert result is not None and len(result) > 0

@pytest.mark.asyncio
async def test_financial_statement_symbol_list():
    result = await financial_statement_symbol_list()
    assert result is not None and len(result) > 0

@pytest.mark.asyncio
async def test_cik_list():
    result = await cik_list()
    assert result is not None and len(result) > 0

@pytest.mark.asyncio
async def test_symbol_change():
    result = await symbol_change()
    assert result is not None and len(result) > 0

@pytest.mark.asyncio
async def test_etf_list():
    result = await etf_list()
    assert result is not None and len(result) > 0

@pytest.mark.asyncio
async def test_actively_trading_list():
    result = await actively_trading_list()
    assert result is not None and len(result) > 0

@pytest.mark.asyncio
async def test_earnings_transcript_list():
    result = await earnings_transcript_list()
    assert result is not None and len(result) > 0

@pytest.mark.asyncio
async def test_available_exchanges():
    result = await available_exchanges()
    assert result is not None and len(result) > 0

@pytest.mark.asyncio
async def test_available_sectors():
    result = await available_sectors()
    assert result is not None and len(result) > 0

@pytest.mark.asyncio
async def test_available_industries():
    result = await available_industries()
    assert result is not None and len(result) > 0

@pytest.mark.asyncio
async def test_available_countries():
    result = await available_countries()
    assert result is not None and len(result) > 0