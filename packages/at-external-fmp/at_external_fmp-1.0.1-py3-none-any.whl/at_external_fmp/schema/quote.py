from pydantic import BaseModel, Field

class Quote(BaseModel):
	symbol: str = Field(..., description="Stock ticker symbol")
	name: str = Field(..., description="Full company or security name")
	price: float = Field(..., description="Current market price")
	changePercentage: float = Field(..., description="Percentage price change from previous close")
	change: float = Field(..., description="Absolute price change from previous close")
	volume: int = Field(..., description="Trading volume for the current session")
	dayLow: float = Field(..., description="Lowest price reached during current trading day")
	dayHigh: float = Field(..., description="Highest price reached during current trading day")
	yearHigh: float = Field(..., description="Highest price reached in the past 52 weeks")
	yearLow: float = Field(..., description="Lowest price reached in the past 52 weeks")
	marketCap: int = Field(..., description="Total market capitalization in base currency")
	priceAvg50: float = Field(..., description="50-day moving average price")
	priceAvg200: float = Field(..., description="200-day moving average price")
	exchange: str = Field(..., description="Name of the exchange where the security is traded")
	open: float = Field(..., description="Opening price for the current trading day")
	previousClose: float = Field(..., description="Closing price from the previous trading day")
	timestamp: int = Field(..., description="Unix timestamp of when the quote was generated")


class QuoteShort(BaseModel):
	symbol: str = Field(..., description="Stock ticker symbol")
	price: float | None = Field(None, description="Current market price if available")
	change: float | None = Field(None, description="Absolute price change from previous close if available")
	volume: int | float | None = Field(None, description="Trading volume for the current session if available")


class AfterMarketTrade(BaseModel):
	symbol: str = Field(..., description="Stock ticker symbol")
	price: float = Field(..., description="Price at which the after-hours trade occurred")
	tradeSize: int = Field(..., description="Number of shares in the after-hours trade")
	timestamp: int = Field(..., description="Unix timestamp of when the trade occurred")

class AfterMarketQuote(BaseModel):
	symbol: str = Field(..., description="Stock ticker symbol")
	bidSize: int = Field(..., description="Number of shares being bid in after-hours")
	bidPrice: float = Field(..., description="Highest price buyers are willing to pay in after-hours")
	askSize: int = Field(..., description="Number of shares being offered in after-hours")
	askPrice: float = Field(..., description="Lowest price sellers are willing to accept in after-hours")
	volume: int = Field(..., description="Total after-hours trading volume")
	timestamp: int = Field(..., description="Unix timestamp of when the after-hours quote was generated")

class PriceChange(BaseModel):
	symbol: str = Field(..., description="Stock ticker symbol")
	oneDay: float = Field(..., alias="1D", description="Percentage price change over the past day")
	fiveDay: float = Field(..., alias="5D", description="Percentage price change over the past 5 trading days")
	oneMonth: float = Field(..., alias="1M", description="Percentage price change over the past month")
	threeMonth: float = Field(..., alias="3M", description="Percentage price change over the past 3 months")
	ytd: float = Field(..., alias="ytd", description="Percentage price change year-to-date")
	oneYear: float = Field(..., alias="1Y", description="Percentage price change over the past year")
	threeYear: float = Field(..., alias="3Y", description="Percentage price change over the past 3 years")
	fiveYear: float = Field(..., alias="5Y", description="Percentage price change over the past 5 years")
	tenYear: float = Field(..., alias="10Y", description="Percentage price change over the past 10 years")
	max: float = Field(..., alias="max", description="Maximum percentage price change since inception")