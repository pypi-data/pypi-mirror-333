from pydantic import BaseModel, Field

class CryptoCurrency(BaseModel):
    symbol: str = Field(..., description="The ticker symbol of the cryptocurrency (e.g., BTC, ETH)")
    name: str = Field(..., description="The full name of the cryptocurrency")
    exchange: str = Field(..., description="The exchange platform where the cryptocurrency is traded")
    icoDate: str | None = Field(None, description="The initial coin offering date in string format, if applicable")
    circulatingSupply: int | float | None = Field(None, description="The number of coins currently in circulation and publicly available")
    totalSupply: int | float | None = Field(None, description="The maximum number of coins that will ever exist for this cryptocurrency")
