from typing import List
from ._client import Client
from .schema.quote import Quote, QuoteShort, AfterMarketTrade, AfterMarketQuote, PriceChange

async def quote(symbol: str) -> List[Quote]:
    """
    Get quote for a stock.
    """
    params = {"symbol": symbol}
    async with Client() as client:
        return [Quote(**item) for item in await client.get("quote", params)]

async def batch_quote(symbols: List[str]) -> List[Quote]:
    """
    Get quote for a list of stocks.
    """
    params = {"symbols": ",".join(symbols)}
    async with Client() as client:
        return [Quote(**item) for item in await client.get("batch-quote", params)]

async def quote_short(symbol: str) -> List[QuoteShort]:
    """
    Get quote for a stock in short format.
    """
    params = {"symbol": symbol}
    async with Client() as client:
        return [QuoteShort(**item) for item in await client.get("quote-short", params)]

async def batch_quote_short(symbols: List[str]) -> List[QuoteShort]:
    """
    Get quote for a list of stocks in short format.
    """
    params = {"symbols": ",".join(symbols)}
    async with Client() as client:
        return [QuoteShort(**item) for item in await client.get("batch-quote-short", params)]

async def aftermarket_trade(symbol: str) -> List[AfterMarketTrade]:
    """
    Get aftermarket trade for a stock.
    """
    params = {"symbol": symbol}
    async with Client() as client:
        return [AfterMarketTrade(**item) for item in await client.get("aftermarket-trade", params)]

async def batch_aftermarket_trade(symbols: List[str]) -> List[AfterMarketTrade]:
    """
    Get aftermarket trade for a list of stocks.
    """
    params = {"symbols": ",".join(symbols)}
    async with Client() as client:
        return [AfterMarketTrade(**item) for item in await client.get("batch-aftermarket-trade", params)]

async def aftermarket_quote(symbol: str) -> List[AfterMarketQuote]:
    """
    Get afterhours quote for a stock.
    """
    params = {"symbol": symbol}
    async with Client() as client:
        return [AfterMarketQuote(**item) for item in await client.get("aftermarket-quote", params)]

async def batch_aftermarket_quote(symbols: List[str]) -> List[AfterMarketQuote]:
    """
    Get afterhours quote for a list of stocks.
    """
    params = {"symbols": ",".join(symbols)}
    async with Client() as client:
        return [AfterMarketQuote(**item) for item in await client.get("batch-aftermarket-quote", params)]

async def stock_price_change(symbol: str) -> List[PriceChange]:
    """
    Get stock price change for a stock.
    """
    params = {"symbol": symbol}
    async with Client() as client:
        return [PriceChange(**item) for item in await client.get("stock-price-change", params)]

async def batch_exchange_quote(exchange: str, short: bool) -> List[QuoteShort]:
    """
    Get exchange quote for a list of stocks.
    """
    params = {"exchange": exchange, "short": short}
    async with Client() as client:
        return [QuoteShort(**item) for item in await client.get("batch-exchange-quote", params)]

async def batch_mutualfund_quotes(short: bool) -> List[QuoteShort]:
    """
    Get mutual fund quotes for a list of mutual funds.
    """
    params = {"short": short}
    async with Client() as client:
        return [QuoteShort(**item) for item in await client.get("batch-mutualfund-quotes", params)]

async def batch_etf_quotes(short: bool) -> List[QuoteShort]:
    """
    Get ETF quotes for a list of ETFs.
    """
    params = {"short": short}
    async with Client() as client:
        return [QuoteShort(**item) for item in await client.get("batch-etf-quotes", params)]

async def batch_crypto_quotes(short: bool) -> List[QuoteShort]:
    """
    Get crypto quotes for a list of cryptocurrencies.
    """
    params = {"short": short}
    async with Client() as client:
        return [QuoteShort(**item) for item in await client.get("batch-crypto-quotes", params)]

async def batch_forex_quotes(short: bool) -> List[QuoteShort]:
    """
    Get forex quotes for a list of forex.
    """
    params = {"short": short}
    async with Client() as client:
        return [QuoteShort(**item) for item in await client.get("batch-forex-quotes", params)]

async def batch_index_quotes(short: bool) -> List[QuoteShort]:
    """
    Get index quotes for a list of indices.
    """
    params = {"short": short}
    async with Client() as client:
        return [QuoteShort(**item) for item in await client.get("batch-index-quotes", params)]