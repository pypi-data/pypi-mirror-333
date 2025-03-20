from pydantic import BaseModel, Field

class SectorPerformanceSnapshot(BaseModel):
    date: str = Field(..., description="Date of the sector performance measurement")
    sector: str = Field(..., description="Name of the market sector")
    exchange: str = Field(..., description="Stock exchange identifier where the sector is tracked")
    averageChange: float = Field(..., description="Average percentage change in value for the sector")

class IndustryPerformanceSnapshot(BaseModel):
    date: str = Field(..., description="Date of the industry performance measurement")
    industry: str = Field(..., description="Name of the specific industry group")
    exchange: str = Field(..., description="Stock exchange identifier where the industry is tracked")
    averageChange: float = Field(..., description="Average percentage change in value for the industry")

class SectorPESnapshot(BaseModel):
    date: str = Field(..., description="Date of the sector PE ratio measurement")
    sector: str = Field(..., description="Name of the market sector")
    exchange: str = Field(..., description="Stock exchange identifier where the sector is tracked")
    pe: float = Field(..., description="Price-to-earnings ratio for the sector")

class IndustryPESnapshot(BaseModel):
    date: str = Field(..., description="Date of the industry PE ratio measurement")
    industry: str = Field(..., description="Name of the specific industry group")
    exchange: str = Field(..., description="Stock exchange identifier where the industry is tracked")
    pe: float = Field(..., description="Price-to-earnings ratio for the industry")

class Stock(BaseModel):
    symbol: str = Field(..., description="Ticker symbol of the stock")
    price: float = Field(..., description="Current market price of the stock")
    name: str = Field(..., description="Full company name")
    change: float = Field(..., description="Absolute price change from previous close")
    changesPercentage: float = Field(..., description="Percentage price change from previous close")
    exchange: str = Field(..., description="Stock exchange identifier where the stock is listed")