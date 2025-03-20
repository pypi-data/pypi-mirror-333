from pydantic import BaseModel, Field

class ESGDisclosureItem(BaseModel):
    date: str = Field(..., description="Date when the ESG disclosure was published")
    acceptedDate: str = Field(..., description="Date when the ESG disclosure was officially accepted or processed")
    symbol: str = Field(..., description="Stock ticker symbol of the company")
    cik: str = Field(..., description="Central Index Key (CIK) identifier assigned by the SEC")
    companyName: str = Field(..., description="Full legal name of the company")
    formType: str = Field(..., description="Type of regulatory form submitted (e.g., 10-K, 10-Q)")
    environmentalScore: float = Field(..., description="Numerical score assessing the company's environmental performance")
    socialScore: float = Field(..., description="Numerical score assessing the company's social responsibility performance")
    governanceScore: float = Field(..., description="Numerical score assessing the company's governance practices")
    ESGScore: float = Field(..., description="Composite score combining environmental, social, and governance metrics")
    url: str = Field(..., description="Web address where the ESG disclosure document can be accessed")

class ESGRatingItem(BaseModel):
    symbol: str = Field(..., description="Stock ticker symbol of the company")
    cik: str = Field(..., description="Central Index Key (CIK) identifier assigned by the SEC")
    companyName: str = Field(..., description="Full legal name of the company")
    industry: str = Field(..., description="Industry classification of the company")
    fiscalYear: int = Field(..., description="Fiscal year for which the ESG rating applies")
    ESGRiskRating: str = Field(..., description="Qualitative assessment of the company's ESG risk level")
    industryRank: str = Field(..., description="Company's ESG performance ranking within its industry")

class ESGBenchmarkItem(BaseModel):
    fiscalYear: int = Field(..., description="Fiscal year for which the benchmark data applies")
    sector: str = Field(..., description="Economic sector classification for the benchmark")
    environmentalScore: float = Field(..., description="Average environmental score for companies in this sector")
    socialScore: float = Field(..., description="Average social responsibility score for companies in this sector")
    governanceScore: float = Field(..., description="Average governance score for companies in this sector")
    ESGScore: float = Field(..., description="Average composite ESG score for companies in this sector")