from typing import List, Optional
from ._client import Client
from .schema.company import (
    CompanyProfile,
    CompanyNote,
    StockPeer,
    DelistedCompany,
    EmployeeCount,
    MarketCapitalization,
    SharesFloat,
    ExecutiveCompensationBenchmark,
    MergerAcquisition,
    Executive,
    ExecutiveCompensation,
    ExecutiveCompensationBenchmark,
)

async def profile(symbol: str) -> List[CompanyProfile]:
    """
    Get company profile information.
    """
    params = {"symbol": symbol}
    async with Client() as client:
        return [CompanyProfile(**item) for item in await client.get("profile", params)]

async def profile_cik(cik: str) -> List[CompanyProfile]:
    """
    Get company profile information by CIK.
    """
    params = {"cik": cik}
    async with Client() as client:
        return [CompanyProfile(**item) for item in await client.get("profile-cik", params)]

async def company_notes(symbol: str) -> List[CompanyNote]:
    """
    Get company notes.
    """
    params = {"symbol": symbol}
    async with Client() as client:
        return [CompanyNote(**item) for item in await client.get("company-notes", params)]

async def stock_peers(symbol: str) -> List[StockPeer]:
    """
    Get stock peers.
    """
    params = {"symbol": symbol}
    async with Client() as client:
        return [StockPeer(**item) for item in await client.get("stock-peers", params)]

async def delisted_companies(page: Optional[int] = None, limit: Optional[int] = None) -> List[DelistedCompany]:
    """
    Get delisted companies.
    """
    params = {}
    if page:
        params["page"] = page
    if limit:
        params["limit"] = limit
    async with Client() as client:
        return [DelistedCompany(**item) for item in await client.get("delisted-companies", params)]

async def employee_count(symbol: str, limit: Optional[int] = None) -> List[EmployeeCount]:
    """
    Get employee count.
    """
    params = {"symbol": symbol}
    if limit:
        params["limit"] = limit
    async with Client() as client:
        return [EmployeeCount(**item) for item in await client.get("employee-count", params)]

async def historical_employee_count(symbol: str, page: Optional[int] = None, limit: Optional[int] = None) -> List[EmployeeCount]:
    """
    Get historical employee count.
    """
    params = {"symbol": symbol}
    if page:
        params["page"] = page
    if limit:
        params["limit"] = limit
    async with Client() as client:
        return [EmployeeCount(**item) for item in await client.get("historical-employee-count", params)]

async def market_capitalization(symbol: str) -> List[MarketCapitalization]:
    """
    Get market capitalization.
    """
    params = {"symbol": symbol}
    async with Client() as client:
        return [MarketCapitalization(**item) for item in await client.get("market-capitalization", params)]

async def market_capitalization_batch(symbols: List[str]) -> List[MarketCapitalization]:
    """
    Get market capitalization for multiple symbols.
    """
    params = {"symbols": ','.join(symbols)}
    async with Client() as client:
        return [MarketCapitalization(**item) for item in await client.get("market-capitalization-batch", params)]

async def historical_market_capitalization(symbol: str, from_date: Optional[str] = None, to_date: Optional[str] = None, limit: Optional[int] = None) -> List[MarketCapitalization]:
    """
    Get historical market capitalization.
    """
    params = {"symbol": symbol}
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date
    if limit:
        params["limit"] = limit
    async with Client() as client:
        return [MarketCapitalization(**item) for item in await client.get("historical-market-capitalization", params)]

async def shares_float(symbol: str) -> List[SharesFloat]:
    """
    Get shares float.
    """
    params = {"symbol": symbol}
    async with Client() as client:
        return [SharesFloat(**item) for item in await client.get("shares-float", params)]

async def shares_float_all() -> List[SharesFloat]:
    """
    Get all shares float.
    """
    async with Client() as client:
        return [SharesFloat(**item) for item in await client.get("shares-float-all")]

async def mergers_acquisitions_latest(page: Optional[int] = None, limit: Optional[int] = None) -> List[MergerAcquisition]:
    """
    Get latest mergers and acquisitions.
    """
    params = {}
    if page:
        params["page"] = page
    if limit:
        params["limit"] = limit
    async with Client() as client:
        return [MergerAcquisition(**item) for item in await client.get("mergers-acquisitions-latest", params)]

async def mergers_acquisitions_search(name: str) -> List[MergerAcquisition]:
    """
    Search for mergers and acquisitions.
    """
    params = {"name": name}
    async with Client() as client:
        return [MergerAcquisition(**item) for item in await client.get("mergers-acquisitions-search", params)]

async def key_executives(symbol: str, active: Optional[bool] = None) -> List[Executive]:
    """
    Get key executives.
    """
    params = {"symbol": symbol}
    if active:
        params["active"] = active
    async with Client() as client:
        return [Executive(**item) for item in await client.get("key-executives", params)]

async def governance_executive_compensation(symbol: str) -> List[ExecutiveCompensation]:
    """
    Get governance executive compensation.
    """
    params = {"symbol": symbol}
    async with Client() as client:
        return [ExecutiveCompensation(**item) for item in await client.get("governance-executive-compensation", params)]

async def executive_compensation_benchmark() -> List[ExecutiveCompensationBenchmark]:
    """
    Get executive compensation benchmark.
    """
    async with Client() as client:
        return [ExecutiveCompensationBenchmark(**item) for item in await client.get("executive-compensation-benchmark")]