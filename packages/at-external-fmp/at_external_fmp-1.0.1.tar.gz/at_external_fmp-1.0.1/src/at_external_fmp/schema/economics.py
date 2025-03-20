from pydantic import BaseModel, Field

class TreasuryRate(BaseModel):
    date: str = Field(..., description="The date for which these U.S. Treasury yield rates are reported")
    month1: float = Field(..., description="The yield rate for 1-month U.S. Treasury securities, expressed as a percentage")
    month2: float = Field(..., description="The yield rate for 2-month U.S. Treasury securities, expressed as a percentage")
    month3: float = Field(..., description="The yield rate for 3-month U.S. Treasury securities, expressed as a percentage")
    month6: float = Field(..., description="The yield rate for 6-month U.S. Treasury securities, expressed as a percentage")
    year1: float = Field(..., description="The yield rate for 1-year U.S. Treasury securities, expressed as a percentage")
    year2: float = Field(..., description="The yield rate for 2-year U.S. Treasury securities, expressed as a percentage")
    year3: float = Field(..., description="The yield rate for 3-year U.S. Treasury securities, expressed as a percentage")
    year5: float = Field(..., description="The yield rate for 5-year U.S. Treasury securities, expressed as a percentage")
    year7: float = Field(..., description="The yield rate for 7-year U.S. Treasury securities, expressed as a percentage")
    year10: float = Field(..., description="The yield rate for 10-year U.S. Treasury securities, expressed as a percentage")
    year20: float = Field(..., description="The yield rate for 20-year U.S. Treasury securities, expressed as a percentage")
    year30: float = Field(..., description="The yield rate for 30-year U.S. Treasury securities, expressed as a percentage")

class EconomicIndicator(BaseModel):
    name: str = Field(..., description="The identifier or name of the economic indicator")
    date: str = Field(..., description="The date associated with the economic indicator measurement")
    value: float = Field(..., description="The numerical value of the economic indicator")

class EconomicCalendarItem(BaseModel):
    event: str = Field(..., description="The name or title of the economic event or data release")
    date: str = Field(..., description="The date when the economic event occurred or is scheduled")
    country: str = Field(..., description="The country or region to which this economic event pertains")
    actual: float | None = Field(None, description="The officially reported value of the economic indicator, if available")
    previous: float | None = Field(None, description="The previously reported value for this economic indicator")
    change: float | None = Field(None, description="The numerical difference between the actual and previous values")
    estimate: float | None = Field(None, description="The consensus forecast value prior to the official release")
    impact: str = Field(..., description="The assessed significance of the economic event's market impact")

class MarketRiskPremiumItem(BaseModel):
    country: str = Field(..., description="The country or market identifier for this risk premium data")
    continent: str = Field(..., description="The continent where the specified country is located")
    countryRiskPremium: float = Field(..., description="The country-specific risk premium component")
    totalEquityRiskPremium: float = Field(..., description="The aggregate equity risk premium for this market")