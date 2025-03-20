import pytest
from at_external_fmp.analyst import *

@pytest.mark.asyncio
async def test_analyst_estimates():
    result = await analyst_estimates("AAPL")
    assert result is not None and len(result) > 0

async def test_ratings_snapshot():
    result = await ratings_snapshot("AAPL")
    assert result is not None and len(result) == 1

async def test_ratings_historical():
    result = await ratings_historical("AAPL")
    assert result is not None and len(result) > 0

async def test_price_target_summary():
    result = await price_target_summary("AAPL")
    assert result is not None and len(result) == 1

async def test_price_target_consensus():
    result = await price_target_consensus("AAPL")
    assert result is not None and len(result) > 0

async def test_price_target_news():
    result = await price_target_news("AAPL", limit=10)
    assert result is not None and len(result) == 10

async def test_price_target_latest_news():
    result = await price_target_latest_news(page=0, limit=10)
    assert result is not None and len(result) <= 10

async def test_grades():
    result = await grades("AAPL")
    assert result is not None and len(result) > 0

async def test_grades_historical():
    result = await grades_historical("AAPL", limit=10)
    assert result is not None and len(result) == 10

async def test_grades_consensus():
    result = await grades_consensus("AAPL")
    assert result is not None and len(result) == 1

async def test_grades_news():
    result = await grades_news("AAPL", limit=10)
    assert result is not None and len(result) <= 10

async def test_grades_latest_news():
    result = await grades_latest_news(page=0, limit=10)
    assert result is not None and len(result) <= 10