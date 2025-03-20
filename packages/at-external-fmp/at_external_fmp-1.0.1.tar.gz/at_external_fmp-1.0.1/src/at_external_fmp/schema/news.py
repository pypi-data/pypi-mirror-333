from pydantic import BaseModel, Field

class FMPArticle(BaseModel):
	title: str = Field(..., description="Title of the financial article")
	date: str = Field(..., description="Publication date of the article")
	content: str = Field(..., description="Full text content of the article")
	tickers: str = Field(..., description="Stock symbols/tickers mentioned in the article")
	image: str = Field(..., description="URL or path to the article's featured image")
	link: str = Field(..., description="URL to the original article")
	author: str = Field(..., description="Name of the article's author")
	site: str = Field(..., description="Source website or publication name")

class NewsItem(BaseModel):
	symbol: str | None = Field(None, description="Stock symbol related to the news item, if applicable")
	publishedDate: str = Field(..., description="Date and time when the news was published")
	publisher: str = Field(..., description="Name of the news publisher or organization")
	title: str = Field(..., description="Headline or title of the news item")
	image: str | None = Field(None, description="URL or path to the news item's featured image, if available")
	site: str = Field(..., description="Source website or platform where the news was published")
	text: str = Field(..., description="Summary or full content of the news item")
	url: str = Field(..., description="Direct link to the original news article")