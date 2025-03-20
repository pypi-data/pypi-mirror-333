from pydantic import BaseModel, Field

class SearchResult(BaseModel):
    symbol: str = Field(..., description="Stock ticker symbol")
    name: str = Field(..., description="Full company name")
    currency: str = Field(..., description="Trading currency code")
    exchangeFullName: str = Field(..., description="Complete name of the stock exchange")
    exchange: str = Field(..., description="Stock exchange code")

class SearchCIKResult(BaseModel):
    symbol: str = Field(..., description="Stock ticker symbol")
    companyName: str = Field(..., description="Full company name")
    cik: str = Field(..., description="Central Index Key (CIK) identifier assigned by the SEC")
    exchangeFullName: str = Field(..., description="Complete name of the stock exchange")
    exchange: str = Field(..., description="Stock exchange code")
    currency: str = Field(..., description="Trading currency code")

class SearchCusipResult(BaseModel):
    symbol: str = Field(..., description="Stock ticker symbol")
    companyName: str = Field(..., description="Full company name")
    cusip: str = Field(..., description="Committee on Uniform Securities Identification Procedures (CUSIP) identifier")
    marketCap: int = Field(..., description="Market capitalization value in the trading currency")

class SearchISINResult(BaseModel):
    symbol: str = Field(..., description="Stock ticker symbol")
    name: str = Field(..., description="Full company name")
    isin: str = Field(..., description="International Securities Identification Number (ISIN)")
    marketCap: int = Field(..., description="Market capitalization value in the trading currency")
    
    