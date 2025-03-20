from pydantic import BaseModel, Field

class ETFHolding(BaseModel):
    symbol: str = Field(..., description="Ticker symbol of the holding")
    asset: str = Field(..., description="Type of asset held in the ETF")
    name: str = Field(..., description="Full name of the holding")
    isin: str = Field(..., description="International Securities Identification Number")
    securityCusip: str = Field(..., description="CUSIP identifier for the security")
    sharesNumber: int | float = Field(..., description="Number of shares of this holding in the ETF")
    weightPercentage: float = Field(..., description="Percentage weight of this holding in the ETF portfolio")
    marketValue: float = Field(..., description="Current market value of this holding")
    updatedAt: str = Field(..., description="Timestamp when this holding data was last updated")
    updated: str = Field(..., description="Date when this holding information was last refreshed")

class ETFInfoSector(BaseModel):
    industry: str = Field(..., description="Name of the industry sector")
    exposure: float = Field(..., description="Percentage exposure to this industry sector")

class ETFInfo(BaseModel):
    symbol: str = Field(..., description="Ticker symbol of the ETF")
    name: str = Field(..., description="Full name of the ETF")
    description: str = Field(..., description="Detailed description of the ETF's investment strategy and objectives")
    isin: str = Field(..., description="International Securities Identification Number")
    assetClass: str = Field(..., description="Primary asset class of the ETF (e.g., equity, fixed income)")
    securityCusip: str = Field(..., description="CUSIP identifier for the ETF")
    domicile: str = Field(..., description="Country where the ETF is legally domiciled")
    website: str = Field(..., description="Official website URL for the ETF")
    etfCompany: str = Field(..., description="Name of the company managing the ETF")
    expenseRatio: float = Field(..., description="Annual management fee as a percentage of assets")
    assetsUnderManagement: float = Field(..., description="Total value of assets managed by the ETF")
    avgVolume: float = Field(..., description="Average daily trading volume")
    inceptionDate: str = Field(..., description="Date when the ETF was first launched")
    nav: float = Field(..., description="Net Asset Value per share")
    navCurrency: str = Field(..., description="Currency in which the NAV is denominated")
    holdingsCount: int = Field(..., description="Total number of individual holdings in the ETF")
    updatedAt: str = Field(..., description="Timestamp when this ETF data was last updated")
    sectorsList: list[ETFInfoSector] = Field(..., description="List of industry sectors and their allocations within the ETF")

class ETFCountryWeight(BaseModel):
    country: str = Field(..., description="Name of the country")
    weightPercentage: str = Field(..., description="Percentage allocation to this country in the ETF")

class ETFAssetExposure(BaseModel):
    symbol: str = Field(..., description="Ticker symbol of the asset")
    asset: str = Field(..., description="Type or name of the asset")
    sharesNumber: int = Field(..., description="Number of shares held of this asset")
    weightPercentage: float = Field(..., description="Percentage weight of this asset in the ETF")
    marketValue: float = Field(..., description="Current market value of this asset holding")

class ETFSectorWeight(BaseModel):
    symbol: str = Field(..., description="Ticker symbol of the ETF")
    sector: str = Field(..., description="Name of the industry sector")
    weightPercentage: float = Field(..., description="Percentage allocation to this sector in the ETF")