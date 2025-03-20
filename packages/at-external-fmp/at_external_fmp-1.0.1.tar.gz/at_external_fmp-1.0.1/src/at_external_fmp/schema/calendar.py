from pydantic import BaseModel, Field

class Dividends(BaseModel):
	symbol: str = Field(..., description="Stock ticker symbol")
	date: str = Field(..., description="Date when the dividend was issued")
	recordDate: str = Field(..., description="Date by which investors must be on company records to receive the dividend")
	paymentDate: str = Field(..., description="Date when the dividend payment is distributed to shareholders")
	declarationDate: str = Field(..., description="Date when the company's board announces the dividend")
	adjDividend: float = Field(..., description="Dividend amount adjusted for stock splits and similar events")
	dividend: float = Field(..., description="Unadjusted dividend amount per share")
	theYield: float = Field(..., alias="yield", description="Annual dividend expressed as a percentage of the stock price")
	frequency: str | None = Field(None, description="How often dividends are paid (e.g., quarterly, annually)")

class Earnings(BaseModel):
	symbol: str = Field(..., description="Stock ticker symbol")
	date: str = Field(..., description="Date of the earnings announcement")
	epsActual: float | None = Field(None, description="Actual earnings per share reported")
	epsEstimated: float | None = Field(None, description="Analysts' consensus estimate for earnings per share")
	revenueActual: float | None = Field(None, description="Actual revenue reported by the company")
	revenueEstimated: float | None = Field(None, description="Analysts' consensus estimate for company revenue")
	lastUpdated: str = Field(..., description="Timestamp of when this earnings data was last updated")

class Splits(BaseModel):
	symbol: str = Field(..., description="Stock ticker symbol")
	date: str = Field(..., description="Date when the stock split occurred")
	numerator: int | float = Field(..., description="Top number in the split ratio (e.g., 2 in a 2:1 split)")
	denominator: int | float = Field(..., description="Bottom number in the split ratio (e.g., 1 in a 2:1 split)")

class IPOs(BaseModel):
	symbol: str = Field(..., description="Stock ticker symbol for the IPO")
	date: str = Field(..., description="Date of the initial public offering")
	daa: str = Field(..., description="Date and time details of the IPO")
	company: str = Field(..., description="Name of the company going public")
	exchange: str = Field(..., description="Stock exchange where the IPO is listed")
	actions: str = Field(..., description="Actions related to the IPO process")
	shares: float | None = Field(None, description="Number of shares offered in the IPO")
	priceRange: str | None = Field(None, description="Expected price range for the IPO shares")
	marketCap: float | None = Field(None, description="Estimated market capitalization at IPO")

class IPOsDisclosure(BaseModel):
	symbol: str = Field(..., description="Stock ticker symbol for the IPO")
	filingDate: str = Field(..., description="Date when IPO documents were filed with regulators")
	acceptedDate: str = Field(..., description="Date when the IPO filing was accepted by regulators")
	effectivenessDate: str = Field(..., description="Date when the IPO registration became effective")
	cik: str = Field(..., description="Central Index Key identifier assigned by the SEC")
	form: str = Field(..., description="Type of regulatory form filed for the IPO")
	url: str = Field(..., description="Link to the IPO disclosure document")

class IPOsProspectus(BaseModel):
	symbol: str = Field(..., description="Stock ticker symbol for the IPO")
	acceptedDate: str = Field(..., description="Date when the prospectus was accepted by regulators")
	filingDate: str = Field(..., description="Date when the prospectus was filed")
	ipoDate: str = Field(..., description="Official date of the initial public offering")
	cik: str = Field(..., description="Central Index Key identifier assigned by the SEC")
	pricePublicPerShare: float = Field(..., description="Offering price per share to the public")
	pricePublicTotal: float = Field(..., description="Total value of shares offered to the public")
	discountsAndCommissionsPerShare: float = Field(..., description="Underwriter fees and commissions per share")
	discountsAndCommissionsTotal: float = Field(..., description="Total underwriter fees and commissions")
	proceedsBeforeExpensesPerShare: float = Field(..., description="Net proceeds per share before other expenses")
	proceedsBeforeExpensesTotal: float = Field(..., description="Total net proceeds before other expenses")
	form: str = Field(..., description="Type of regulatory form containing the prospectus")
	url: str = Field(..., description="Link to the prospectus document")