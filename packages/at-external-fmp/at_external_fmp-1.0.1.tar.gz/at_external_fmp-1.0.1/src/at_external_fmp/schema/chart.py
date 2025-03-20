from pydantic import BaseModel, Field

class PriceEODLight(BaseModel):
    symbol: str = Field(..., description="Stock ticker symbol")
    date: str = Field(..., description="Date of the price data")
    price: float = Field(..., description="Stock price value")
    volume: int = Field(..., description="Trading volume for the day")

class PriceEODFull(BaseModel):
    symbol: str = Field(..., description="Stock ticker symbol")
    date: str = Field(..., description="Date of the price data")
    open: float = Field(..., description="Opening price for the trading day")
    high: float = Field(..., description="Highest price reached during the trading day")
    low: float = Field(..., description="Lowest price reached during the trading day")
    close: float = Field(..., description="Closing price for the trading day")
    volume: int = Field(..., description="Trading volume for the day")
    change: float = Field(..., description="Absolute price change from previous day")
    changePercent: float = Field(..., description="Percentage price change from previous day")
    vwap: float = Field(..., description="Volume Weighted Average Price for the day")

class PriceEODAdjusted(BaseModel):
    symbol: str = Field(..., description="Stock ticker symbol")
    date: str = Field(..., description="Date of the price data")
    adjOpen: float = Field(..., description="Adjusted opening price accounting for corporate actions")
    adjHigh: float = Field(..., description="Adjusted highest price accounting for corporate actions")
    adjLow: float = Field(..., description="Adjusted lowest price accounting for corporate actions")
    adjClose: float = Field(..., description="Adjusted closing price accounting for corporate actions")
    volume: int = Field(..., description="Trading volume for the day")

class PriceIntraday(BaseModel):
    date: str = Field(..., description="Timestamp of the intraday price data")
    open: float = Field(..., description="Opening price for the time interval")
    low: float = Field(..., description="Lowest price during the time interval")
    high: float = Field(..., description="Highest price during the time interval")
    close: float = Field(..., description="Closing price for the time interval")
    volume: int = Field(..., description="Trading volume for the time interval")