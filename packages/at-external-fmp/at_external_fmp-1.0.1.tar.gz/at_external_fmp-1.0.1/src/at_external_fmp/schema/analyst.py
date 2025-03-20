from pydantic import BaseModel, Field

class AnalystEstimates(BaseModel):
    symbol: str = Field(..., description="Stock ticker symbol")
    date: str = Field(..., description="Date when the estimate was published")
    revenueLow: float = Field(..., description="Lowest revenue estimate among analysts")
    revenueHigh: float = Field(..., description="Highest revenue estimate among analysts")
    revenueAvg: float = Field(..., description="Average of all analyst revenue estimates")
    ebitdaLow: float = Field(..., description="Lowest EBITDA (Earnings Before Interest, Taxes, Depreciation, and Amortization) estimate")
    ebitdaHigh: float = Field(..., description="Highest EBITDA estimate")
    ebitdaAvg: float = Field(..., description="Average of all analyst EBITDA estimates")
    ebitLow: float = Field(..., description="Lowest EBIT (Earnings Before Interest and Taxes) estimate")
    ebitHigh: float = Field(..., description="Highest EBIT estimate")
    ebitAvg: float = Field(..., description="Average of all analyst EBIT estimates")
    netIncomeLow: float = Field(..., description="Lowest net income estimate")
    netIncomeHigh: float = Field(..., description="Highest net income estimate")
    netIncomeAvg: float = Field(..., description="Average of all analyst net income estimates")
    sgaExpenseLow: float = Field(..., description="Lowest SG&A (Selling, General & Administrative) expense estimate")
    sgaExpenseHigh: float = Field(..., description="Highest SG&A expense estimate")
    sgaExpenseAvg: float = Field(..., description="Average of all analyst SG&A expense estimates")
    epsAvg: float = Field(..., description="Average of all analyst EPS (Earnings Per Share) estimates")
    epsHigh: float = Field(..., description="Highest EPS estimate")
    epsLow: float = Field(..., description="Lowest EPS estimate")
    numAnalystsRevenue: int = Field(..., description="Number of analysts contributing to revenue estimates")
    numAnalystsEps: int = Field(..., description="Number of analysts contributing to EPS estimates")

class RatingsSnapshot(BaseModel):
    symbol: str = Field(..., description="Stock ticker symbol")
    rating: str = Field(..., description="Overall analyst rating classification")
    overallScore: int = Field(..., description="Composite score based on all rating factors")
    discountedCashFlowScore: int = Field(..., description="Score based on discounted cash flow analysis")
    returnOnEquityScore: int = Field(..., description="Score based on company's return on equity metrics")
    returnOnAssetsScore: int = Field(..., description="Score based on company's return on assets performance")
    debtToEquityScore: int = Field(..., description="Score based on company's debt to equity ratio")
    priceToEarningsScore: int = Field(..., description="Score based on stock's price to earnings ratio")
    priceToBookScore: int = Field(..., description="Score based on stock's price to book ratio")

class RatingsHistorical(RatingsSnapshot):
    date: str = Field(..., description="Date when the rating was issued")

class PriceTargetSummary(BaseModel):
    symbol: str = Field(..., description="Stock ticker symbol")
    lastMonthCount: int = Field(..., description="Number of price targets issued in the past month")
    lastMonthAvgPriceTarget: float = Field(..., description="Average of price targets from the past month")
    lastQuarterCount: int = Field(..., description="Number of price targets issued in the past quarter")
    lastQuarterAvgPriceTarget: float = Field(..., description="Average of price targets from the past quarter")
    lastYearCount: int = Field(..., description="Number of price targets issued in the past year")
    lastYearAvgPriceTarget: float = Field(..., description="Average of price targets from the past year")
    allTimeCount: int = Field(..., description="Total number of price targets in the dataset")
    allTimeAvgPriceTarget: float = Field(..., description="Average of all price targets in the dataset")
    publishers: str = Field(..., description="List of financial institutions that published these price targets")

class PriceTargetConsensus(BaseModel):
    symbol: str = Field(..., description="Stock ticker symbol")
    targetHigh: float = Field(..., description="Highest analyst price target currently active")
    targetLow: float = Field(..., description="Lowest analyst price target currently active")
    targetConsensus: float = Field(..., description="Average of all current analyst price targets")
    targetMedian: float = Field(..., description="Median value of all current analyst price targets")

class PriceTargetNews(BaseModel):
    symbol: str = Field(..., description="Stock ticker symbol")
    publishedDate: str = Field(..., description="Date when the price target was published")
    newsURL: str = Field(..., description="Full URL to the news article containing the price target")
    newsTitle: str = Field(..., description="Title of the news article")
    analystName: str = Field(..., description="Name of the analyst who issued the price target")
    priceTarget: float = Field(..., description="Price target value issued by the analyst")
    adjPriceTarget: float = Field(..., description="Price target adjusted for stock splits or other events")
    priceWhenPosted: float = Field(..., description="Stock price at the time the price target was published")
    newsPublisher: str = Field(..., description="Name of the media outlet that published the article")
    newsBaseURL: str = Field(..., description="Base domain of the news source")
    analystCompany: str = Field(..., description="Financial institution the analyst works for")    

class Grades(BaseModel):
    symbol: str = Field(..., description="Stock ticker symbol")
    date: str = Field(..., description="Date when the grade was issued")
    gradingCompany: str = Field(..., description="Financial institution that issued the grade")
    previousGrade: str = Field(..., description="Previous rating assigned to the stock by this institution")
    newGrade: str = Field(..., description="New rating assigned to the stock by this institution")
    action: str = Field(..., description="Type of rating change (upgrade, downgrade, initiation, etc.)")

class GradesHistorical(BaseModel):
    symbol: str = Field(..., description="Stock ticker symbol")
    date: str = Field(..., description="Date of the historical rating snapshot")
    analystRatingsBuy: int = Field(..., description="Number of Buy ratings at this point in time")
    analystRatingsHold: int = Field(..., description="Number of Hold ratings at this point in time")
    analystRatingsSell: int = Field(..., description="Number of Sell ratings at this point in time")
    analystRatingsStrongSell: int = Field(..., description="Number of Strong Sell ratings at this point in time")

class GradesConsensus(BaseModel):
    symbol: str = Field(..., description="Stock ticker symbol")
    strongBuy: int = Field(..., description="Current number of Strong Buy ratings")
    buy: int = Field(..., description="Current number of Buy ratings")
    hold: int = Field(..., description="Current number of Hold ratings")
    sell: int = Field(..., description="Current number of Sell ratings")
    strongSell: int = Field(..., description="Current number of Strong Sell ratings")
    consensus: str = Field(..., description="Overall consensus rating based on all analyst ratings")

class GradesNews(BaseModel):
    symbol: str = Field(..., description="Stock ticker symbol")
    publishedDate: str = Field(..., description="Date when the rating news was published")
    newsURL: str = Field(..., description="Full URL to the news article about the rating")
    newsTitle: str = Field(..., description="Title of the news article")
    newsBaseURL: str = Field(..., description="Base domain of the news source")
    newsPublisher: str = Field(..., description="Name of the media outlet that published the article")
    newGrade: str = Field(..., description="New rating assigned to the stock")
    previousGrade: str | None = Field(None, description="Previous rating assigned to the stock, if available")
    gradingCompany: str = Field(..., description="Financial institution that issued the rating")
    action: str = Field(..., description="Type of rating action (upgrade, downgrade, initiation, etc.)")
    priceWhenPosted: float = Field(..., description="Stock price at the time the rating was published")