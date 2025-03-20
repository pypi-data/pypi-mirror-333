from pydantic import BaseModel, Field

class ForexItem(BaseModel):
    symbol: str = Field(..., description="The trading symbol representing the currency pair")
    fromCurrency: str = Field(..., description="The base currency code in the currency pair")
    toCurrency: str = Field(..., description="The quote currency code in the currency pair")
    fromName: str = Field(..., description="The full name of the base currency")
    toName: str = Field(..., description="The full name of the quote currency")