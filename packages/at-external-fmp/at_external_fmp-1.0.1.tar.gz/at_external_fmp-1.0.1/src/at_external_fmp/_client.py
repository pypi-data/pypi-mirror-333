"""
API client module for making requests to the Financial Modeling Prep API.
"""
from typing import Dict, Any, Optional
import httpx, os, asyncio, time, logging
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get API key from environment variable
API_KEY = os.environ.get("FMP_API_KEY", "")
BASE_URL = "https://financialmodelingprep.com/stable"

# Rate limiting configuration
RATE_LIMIT = 5  # Maximum requests per second
RATE_LIMIT_PERIOD = 1.0  # Period in seconds

class RateLimiter:
    """
    Rate limiter to prevent exceeding API rate limits.
    """
    def __init__(self, rate_limit: int, period: float):
        """
        Initialize the rate limiter.
        
        Args:
            rate_limit: Maximum number of requests allowed in the period
            period: Time period in seconds
        """
        self.rate_limit = rate_limit
        self.period = period
        self.timestamps = []
        self._lock = asyncio.Lock()
    
    async def acquire(self):
        """
        Acquire permission to make a request, waiting if necessary.
        """
        async with self._lock:
            now = time.time()
            
            # Remove timestamps older than the period
            self.timestamps = [ts for ts in self.timestamps if now - ts < self.period]
            
            # If we've reached the rate limit, wait until we can make another request
            if len(self.timestamps) >= self.rate_limit:
                wait_time = self.period - (now - self.timestamps[0])
                if wait_time > 0:
                    logger.debug(f"Rate limit reached, waiting for {wait_time:.2f} seconds")
                    await asyncio.sleep(wait_time)
                    now = time.time()  # Update current time after waiting
            
            # Add current timestamp and allow the request
            self.timestamps.append(now)

class Client:
    """
    Client for making requests to the Financial Modeling Prep API.
    """
    _instance = None
    _client = None
    _rate_limiter = None
    
    def __new__(cls):
        """
        Implement singleton pattern to ensure only one client instance exists.
        """
        if cls._instance is None:
            cls._instance = super(Client, cls).__new__(cls)
            # Initialize rate limiter
            cls._rate_limiter = RateLimiter(RATE_LIMIT, RATE_LIMIT_PERIOD)
        return cls._instance
    
    def _ensure_client(self):
        """
        Ensure the HTTP client is initialized.
        """
        if self._client is None:
            self._client = httpx.AsyncClient(
                timeout=30.0,  # 30 second timeout
                limits=httpx.Limits(
                    max_keepalive_connections=10,
                    max_connections=20,
                    keepalive_expiry=60.0  # 60 seconds
                ),
                headers={"Accept-Encoding": "gzip, deflate"}  # Enable compression
            )
    
    async def close(self):
        """
        Close the HTTP client.
        """
        if self._client:
            await self._client.aclose()
            self._client = None
    
    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type((httpx.RequestError, httpx.HTTPStatusError)),
        reraise=True
    )
    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """
        Make a GET request to the API with retry logic and rate limiting.
        
        Args:
            endpoint: API endpoint path
            params: Query parameters for the request
            
        Returns:
            JSON response from the API
            
        Raises:
            httpx.HTTPStatusError: If the request fails with a 4xx or 5xx status code
            httpx.RequestError: If the request fails due to connection issues
        """
        # Initialize params if None
        if params is None:
            params = {}
            
        # Ensure API key is included in all requests
        params["apikey"] = API_KEY
        
        # Apply rate limiting
        await self._rate_limiter.acquire()
        
        # Ensure client is initialized
        self._ensure_client()
        
        try:
            # Make the request
            url = f"{BASE_URL}/{endpoint}"
            logger.debug(f"Making GET request to {url} with params {params}")
            
            response = await self._client.get(url, params=params)
            response.raise_for_status()
            
            # Log successful response and compression info
            content_encoding = response.headers.get("Content-Encoding", "none")
            logger.debug(f"Received response from {url}: {response.status_code} (Encoding: {content_encoding})")
            
            return response.json()
        except httpx.HTTPStatusError as e:
            # Handle HTTP errors (4xx, 5xx)
            logger.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            
            # Handle rate limiting specifically (usually 429 Too Many Requests)
            if e.response.status_code == httpx.codes.TOO_MANY_REQUESTS:
                retry_after = int(e.response.headers.get("Retry-After", 5))
                logger.warning(f"Rate limit exceeded. Retrying after {retry_after} seconds")
                await asyncio.sleep(retry_after)
            
            raise
        except httpx.RequestError as e:
            # Handle network/connection errors
            logger.error(f"Request error occurred: {str(e)}")
            raise
        except Exception as e:
            # Handle unexpected errors
            logger.error(f"Unexpected error occurred: {str(e)}")
            raise
    # Context manager support
    async def __aenter__(self):
        self._ensure_client()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()