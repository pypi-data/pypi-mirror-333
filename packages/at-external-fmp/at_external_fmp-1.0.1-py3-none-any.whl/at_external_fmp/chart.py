from typing import List, Optional
from ._client import Client
from .schema.chart import (
    PriceEODLight, PriceEODFull, PriceEODAdjusted, PriceIntraday
)

async def historical_price_eod_light(symbol: str, from_date: Optional[str] = None, to_date: Optional[str] = None) -> List[PriceEODLight]:
    """
    Get lightweight historical end-of-day price data for a symbol.
    """
    params = {
        "symbol": symbol
    }
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date
    async with Client() as client:
        return [PriceEODLight(**item) for item in await client.get("historical-price-eod/light", params)]

async def historical_price_eod_full(symbol: str, from_date: str, to_date: str) -> List[PriceEODFull]:
    """
    Get comprehensive historical end-of-day price data for a symbol.
    """
    params = {
        "symbol": symbol
    }
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date
    async with Client() as client:
        return [PriceEODFull(**item) for item in await client.get("historical-price-eod/full", params)]

async def historical_price_eod_non_split_adjusted(symbol: str, from_date: Optional[str] = None, to_date: Optional[str] = None) -> List[PriceEODAdjusted]:
    """
    Get historical end-of-day price data without stock split adjustments.
    """
    params = {
        "symbol": symbol
    }
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date
    async with Client() as client:
        return [PriceEODAdjusted(**item) for item in await client.get("historical-price-eod/non-split-adjusted", params)]

async def historical_price_eod_dividend_adjusted(symbol: str, from_date: Optional[str] = None, to_date: Optional[str] = None) -> List[PriceEODAdjusted]:
    """
    Get historical end-of-day price data with dividend adjustments.
    """
    params = {
        "symbol": symbol
    }
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date
    async with Client() as client:
        return [PriceEODAdjusted(**item) for item in await client.get("historical-price-eod/dividend-adjusted", params)]

async def historical_chart_5min(symbol: str, from_date: Optional[str] = None, to_date: Optional[str] = None, non_adjusted: Optional[bool] = False) -> List[PriceIntraday]:
    """
    Get historical 5-minute price data for a symbol.
    """
    params = {
        "symbol": symbol
    }
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date
    if non_adjusted:
        params["non_adjusted"] = non_adjusted
    async with Client() as client:
        return [PriceIntraday(**item) for item in await client.get("historical-chart/5min", params)]

async def historical_chart_15min(symbol: str, from_date: Optional[str] = None, to_date: Optional[str] = None, non_adjusted: Optional[bool] = False) -> List[PriceIntraday]:
    """
    Get historical 15-minute price data for a symbol.
    """
    params = {
        "symbol": symbol
    }
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date
    if non_adjusted:
        params["non_adjusted"] = non_adjusted
    async with Client() as client:
        return [PriceIntraday(**item) for item in await client.get("historical-chart/15min", params)]

async def historical_chart_30min(symbol: str, from_date: Optional[str] = None, to_date: Optional[str] = None, non_adjusted: Optional[bool] = False) -> List[PriceIntraday]:
    """
    Get historical 30-minute price data for a symbol.
    """
    params = {
        "symbol": symbol
    }
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date
    if non_adjusted:
        params["non_adjusted"] = non_adjusted
    async with Client() as client:
        return [PriceIntraday(**item) for item in await client.get("historical-chart/30min", params)]

async def historical_chart_1hr(symbol: str, from_date: Optional[str] = None, to_date: Optional[str] = None, non_adjusted: Optional[bool] = False) -> List[PriceIntraday]:
    """
    Get historical 1-hour price data for a symbol.
    """
    params = {
        "symbol": symbol
    }
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date
    if non_adjusted:
        params["non_adjusted"] = non_adjusted
    async with Client() as client:
        return [PriceIntraday(**item) for item in await client.get("historical-chart/1hour", params)]

async def historical_chart_4hr(symbol: str, from_date: Optional[str] = None, to_date: Optional[str] = None, non_adjusted: Optional[bool] = False) -> List[PriceIntraday]:
    """
    Get historical 4-hour price data for a symbol.
    """
    params = {
        "symbol": symbol
    }
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date
    if non_adjusted:
        params["non_adjusted"] = non_adjusted
    async with Client() as client:
        return [PriceIntraday(**item) for item in await client.get("historical-chart/4hour", params)]

