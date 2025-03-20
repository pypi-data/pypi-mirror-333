from typing import List, Optional
from ._client import Client
from .schema.directory import (
    StockItem, FinancialStatementSymbolItem, CIKItem, SymbolChangeItem, EarningsTranscriptItem, ExchangeItem, SectorItem, IndustryItem, CountryItem
)

async def stock_list() -> List[StockItem]:
    """
    Get a list of all stocks.
    """
    async with Client() as client:
        return [StockItem(**item) for item in await client.get("stock-list")]

async def financial_statement_symbol_list() -> List[FinancialStatementSymbolItem]:
    """
    Get a list of all financial statement symbols.
    """
    async with Client() as client:
        return [FinancialStatementSymbolItem(**item) for item in await client.get("financial-statement-symbol-list")]

async def cik_list(limit: Optional[int] = None) -> List[CIKItem]:
    """
    Get a list of all CIKs.
    """
    params = {}
    if limit:
        params["limit"] = limit
    async with Client() as client:
        return [CIKItem(**item) for item in await client.get("cik-list", params)]

async def symbol_change() -> List[SymbolChangeItem]:
    """
    Get a list of all symbol changes.
    """
    async with Client() as client:
        return [SymbolChangeItem(**item) for item in await client.get("symbol-change")]

async def etf_list() -> List[StockItem]:
    """
    Get a list of all ETFs.
    """
    async with Client() as client:
        return [StockItem(**item) for item in await client.get("etf-list")]

async def actively_trading_list() -> List[StockItem]:
    """
    Get a list of all actively trading stocks.
    """
    async with Client() as client:
        return [StockItem(**item) for item in await client.get("actively-trading-list")]

async def earnings_transcript_list() -> List[EarningsTranscriptItem]:
    """
    Get a list of all earnings transcripts.
    """
    async with Client() as client:
        return [EarningsTranscriptItem(**item) for item in await client.get("earnings-transcript-list")]

async def available_exchanges() -> List[ExchangeItem]:
    """
    Get a list of all available exchanges.
    """
    async with Client() as client:
        return [ExchangeItem(**item) for item in await client.get("available-exchanges")]

async def available_sectors() -> List[SectorItem]:
    """
    Get a list of all available sectors.
    """
    async with Client() as client:
        return [SectorItem(**item) for item in await client.get("available-sectors")]

async def available_industries() -> List[IndustryItem]:
    """
    Get a list of all available industries.
    """
    async with Client() as client:
        return [IndustryItem(**item) for item in await client.get("available-industries")]

async def available_countries() -> List[CountryItem]:
    """
    Get a list of all available countries.
    """
    async with Client() as client:
        return [CountryItem(**item) for item in await client.get("available-countries")]

