from pydantic import BaseModel, Field, AliasChoices

class StockItem(BaseModel):
    symbol: str = Field(..., description="Stock ticker symbol used for trading identification")
    name: str = Field(..., description="Official company or entity name", validation_alias=AliasChoices('companyName', 'name'))

class FinancialStatementSymbolItem(BaseModel):
    symbol: str = Field(..., description="Stock ticker symbol used for trading identification")
    companyName: str = Field(..., description="Official company or entity name")
    tradingCurrency: str | None = Field(None, description="Currency code used for stock trading transactions")
    reportingCurrency: str | None = Field(None, description="Currency code used in the company's financial statements")

class CIKItem(BaseModel):
    cik: str = Field(..., description="Central Index Key (CIK) unique identifier assigned by the SEC to entities that file disclosures")
    companyName: str = Field(..., description="Official company or entity name")

class SymbolChangeItem(BaseModel):
    date: str = Field(..., description="Date when the ticker symbol change occurred")
    companyName: str = Field(..., description="Official company or entity name")
    oldSymbol: str = Field(..., description="Previous ticker symbol before the change")
    newSymbol: str = Field(..., description="Current ticker symbol after the change")

class EarningsTranscriptItem(BaseModel):
    symbol: str = Field(..., description="Stock ticker symbol used for trading identification")
    companyName: str = Field(..., description="Official company or entity name")
    noOfTranscripts: int = Field(..., description="Total count of available earnings call transcripts")

class ExchangeItem(BaseModel):
    exchange: str = Field(..., description="Stock exchange code or identifier where securities are traded")

class SectorItem(BaseModel):
    sector: str = Field(..., description="Broad market sector classification for categorizing companies")

class IndustryItem(BaseModel):
    industry: str = Field(..., description="Specific industry classification within a broader sector")

class CountryItem(BaseModel):
    country: str = Field(..., description="Country name where the company is headquartered or registered")