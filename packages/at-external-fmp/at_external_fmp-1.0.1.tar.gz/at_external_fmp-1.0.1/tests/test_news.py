import pytest
from at_external_fmp.news import *

@pytest.mark.asyncio
async def test_fmp_articles():
    result = await fmp_articles()
    assert result is not None and len(result) > 0

@pytest.mark.asyncio
async def test_news_general_latest():
    result = await news_general_latest(page=0, limit=10)
    assert result is not None and len(result) == 10

@pytest.mark.asyncio
async def test_news_stock_latest():
    result = await news_stock_latest(page=0, limit=10)
    assert result is not None and len(result) == 10

@pytest.mark.asyncio
async def test_news_crypto_latest():
    result = await news_crypto_latest(page=0, limit=10)
    assert result is not None and len(result) == 10

@pytest.mark.asyncio
async def test_news_forex_latest():
    result = await news_forex_latest(page=0, limit=10)
    assert result is not None and len(result) == 10

@pytest.mark.asyncio
async def test_news_stock():
    result = await news_stock(symbols=["AAPL"], page=0, limit=10)
    assert result is not None and len(result) == 10

@pytest.mark.asyncio
async def test_news_crypto():
    result = await news_crypto(symbols=["BTCUSD"], page=0, limit=10)
    assert result is not None and len(result) == 10

@pytest.mark.asyncio
async def test_news_forex():
    result = await news_forex(symbols=["EURUSD"], page=0, limit=10)
    assert result is not None and len(result) == 10