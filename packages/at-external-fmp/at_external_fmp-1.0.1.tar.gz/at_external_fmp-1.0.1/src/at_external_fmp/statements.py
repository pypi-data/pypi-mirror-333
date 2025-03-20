from typing import List, Dict, Any, Optional
from ._client import Client
from .schema.statements import (
    IncomeStatement, IncomeStatementGrowth, 
    BalanceSheetStatement, BalanceSheetStatementGrowth, 
    CashFlowStatement, CashFlowStatementGrowth, 
    FinancialGrowth, 
    KeyMetrics, KeyMetricsTTM, 
    Ratios, RatiosTTM, 
    FinancialScores, OwnerEarnings, EnterpriseValues
)

async def income_statement(symbol: str, period: Optional[str] = None, limit: Optional[int] = None) -> List[IncomeStatement]:
    """
    Get income statement for a symbol.
    period: QUARTER/FY
    """
    params = {"symbol": symbol}
    if period:
        params["period"] = period
    if limit:
        params["limit"] = limit
    async with Client() as client:
        return [IncomeStatement(**item) for item in await client.get("income-statement", params)]

async def income_statement_growth(symbol: str, period: Optional[str] = None, limit: Optional[int] = None) -> List[IncomeStatementGrowth]:
    """
    Get income statement growth for a symbol.
    period: QUARTER/FY
    """
    params = {"symbol": symbol}
    if period:
        params["period"] = period
    if limit:
        params["limit"] = limit
    async with Client() as client:
        return [IncomeStatementGrowth(**item) for item in await client.get("income-statement-growth", params)]

async def balance_sheet_statement(symbol: str, period: Optional[str] = None, limit: Optional[int] = None) -> List[BalanceSheetStatement]:
    """
    Get balance sheet statement for a symbol.
    period: QUARTER/FY
    """
    params = {"symbol": symbol}
    if period:
        params["period"] = period
    if limit:
        params["limit"] = limit
    async with Client() as client:
        return [BalanceSheetStatement(**item) for item in await client.get("balance-sheet-statement", params)]

async def balance_sheet_statement_growth(symbol: str, period: Optional[str] = None, limit: Optional[int] = None) -> List[BalanceSheetStatementGrowth]:
    """
    Get balance sheet statement growth for a symbol.
    period: QUARTER/FY
    """
    params = {"symbol": symbol}
    if period:
        params["period"] = period
    if limit:
        params["limit"] = limit
    async with Client() as client:
        return [BalanceSheetStatementGrowth(**item) for item in await client.get("balance-sheet-statement-growth", params)]

async def cash_flow_statement(symbol: str, period: Optional[str] = None, limit: Optional[int] = None) -> List[CashFlowStatement]:
    """
    Get cash flow statement for a symbol.
    period: QUARTER/FY
    """
    params = {"symbol": symbol}
    if period:
        params["period"] = period
    if limit:
        params["limit"] = limit
    async with Client() as client:
        return [CashFlowStatement(**item) for item in await client.get("cash-flow-statement", params)]

async def cash_flow_statement_growth(symbol: str, period: Optional[str] = None, limit: Optional[int] = None) -> List[CashFlowStatementGrowth]:
    """
    Get cash flow statement growth for a symbol.
    period: QUARTER/FY
    """
    params = {"symbol": symbol}
    if period:
        params["period"] = period
    if limit:
        params["limit"] = limit
    async with Client() as client:
        return [CashFlowStatementGrowth(**item) for item in await client.get("cash-flow-statement-growth", params)]

async def financial_growth(symbol: str, period: Optional[str] = None, limit: Optional[int] = None) -> List[FinancialGrowth]:
    """
    Get financial growth for a symbol.
    period: QUARTER/FY
    """
    params = {"symbol": symbol}
    if period:
        params["period"] = period
    if limit:
        params["limit"] = limit
    async with Client() as client:
        return [FinancialGrowth(**item) for item in await client.get("financial-growth", params)]

async def key_metrics(symbol: str, period: Optional[str] = None, limit: Optional[int] = None) -> List[KeyMetrics]:
    """
    Get key metrics for a symbol.
    period: QUARTER/FY
    """
    params = {"symbol": symbol}
    if period:
        params["period"] = period
    if limit:
        params["limit"] = limit
    async with Client() as client:
        return [KeyMetrics(**item) for item in await client.get("key-metrics", params)]

async def key_metrics_ttm(symbol: str) -> List[KeyMetricsTTM]:
    """
    Get key metrics for a symbol using trailing twelve months (TTM) data.
    """
    params = {"symbol": symbol}
    async with Client() as client:
        return [KeyMetricsTTM(**item) for item in await client.get("key-metrics-ttm", params)]

async def ratios(symbol: str, period: Optional[str] = None, limit: Optional[int] = None) -> List[Ratios]:
    """
    Get ratios for a symbol.
    period: QUARTER/FY
    """
    params = {"symbol": symbol}
    if period:
        params["period"] = period
    if limit:
        params["limit"] = limit
    async with Client() as client:
        return [Ratios(**item) for item in await client.get("ratios", params)]

async def ratios_ttm(symbol: str) -> List[RatiosTTM]:
    """
    Get ratios for a symbol using trailing twelve months (TTM) data.
    """
    params = {"symbol": symbol}
    async with Client() as client:
        return [RatiosTTM(**item) for item in await client.get("ratios-ttm", params)]

async def financial_scores(symbol: str) -> List[FinancialScores]:
    """
    Get financial scores for a symbol.
    """
    params = {"symbol": symbol}
    async with Client() as client:
        return [FinancialScores(**item) for item in await client.get("financial-scores", params)]

async def owner_earnings(symbol: str, limit: Optional[int] = None) -> List[OwnerEarnings]:
    """
    Get owner earnings for a symbol.
    """
    params = {"symbol": symbol}
    if limit:
        params["limit"] = limit
    async with Client() as client:
        return [OwnerEarnings(**item) for item in await client.get("owner-earnings", params)]

async def enterprise_values(symbol: str, period: Optional[str] = None, limit: Optional[int] = None) -> List[EnterpriseValues]:
    """
    Get enterprise value for a symbol.
    period: annual
    """
    params = {"symbol": symbol}
    if period:
        params["period"] = period
    if limit:
        params["limit"] = limit
    async with Client() as client:
        return [EnterpriseValues(**item) for item in await client.get("enterprise-values", params)]
