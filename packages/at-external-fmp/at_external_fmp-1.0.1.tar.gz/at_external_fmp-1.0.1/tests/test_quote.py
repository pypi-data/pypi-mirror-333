import pytest
from at_external_fmp.quote import *

@pytest.mark.asyncio
async def test_quote():
    result = await quote("AAPL")
    assert result is not None and len(result) == 1

@pytest.mark.asyncio
async def test_batch_quote():
    result = await batch_quote(["AAPL", "GOOG"])
    assert result is not None and len(result) == 2

@pytest.mark.asyncio
async def test_quote_short():
    result = await quote_short("AAPL")
    assert result is not None and len(result) == 1

@pytest.mark.asyncio
async def test_batch_quote_short():
    result = await batch_quote_short(["AAPL", "GOOG"])
    assert result is not None and len(result) == 2

@pytest.mark.asyncio
async def test_aftermarket_trade():
    result = await aftermarket_trade("AAPL")
    assert result is not None and len(result) == 1

@pytest.mark.asyncio
async def test_batch_aftermarket_trade():
    result = await batch_aftermarket_trade(["AAPL", "GOOG"])
    assert result is not None and len(result) == 2

@pytest.mark.asyncio
async def test_aftermarket_quote():
    result = await aftermarket_quote("AAPL")
    assert result is not None and len(result) == 1

@pytest.mark.asyncio
async def test_batch_aftermarket_quote():
    result = await batch_aftermarket_quote(["AAPL", "GOOG"])
    assert result is not None and len(result) == 2

@pytest.mark.asyncio
async def test_stock_price_change():
    result = await stock_price_change("AAPL")
    assert result is not None and len(result) == 1
        
@pytest.mark.asyncio
async def test_batch_exchange_quote():
    result = await batch_exchange_quote(exchange="NASDAQ", short=True)
    assert result is not None and len(result) > 0

    result = await batch_exchange_quote(exchange="NASDAQ", short=False)
    assert result is not None and len(result) > 0

@pytest.mark.asyncio
async def test_batch_mutualfund_quotes():
    result = await batch_mutualfund_quotes(short=True)
    assert result is not None and len(result) > 0

    result = await batch_mutualfund_quotes(short=False)
    assert result is not None and len(result) > 0

@pytest.mark.asyncio
async def test_batch_etf_quotes():
    result = await batch_etf_quotes(short=True)
    assert result is not None and len(result) > 0

    result = await batch_etf_quotes(short=False)
    assert result is not None and len(result) > 0

@pytest.mark.asyncio
async def test_batch_crypto_quotes():
    result = await batch_crypto_quotes(short=True)
    assert result is not None and len(result) > 0

    result = await batch_crypto_quotes(short=False)
    assert result is not None and len(result) > 0


@pytest.mark.asyncio
async def test_batch_forex_quotes():
    result = await batch_forex_quotes(short=True)
    assert result is not None and len(result) > 0

    result = await batch_forex_quotes(short=False)
    assert result is not None and len(result) > 0

@pytest.mark.asyncio
async def test_batch_index_quotes():
    result = await batch_index_quotes(short=True)
    assert result is not None and len(result) > 0

    result = await batch_index_quotes(short=False)
    assert result is not None and len(result) > 0
    