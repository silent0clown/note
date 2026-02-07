from abc import ABC, abstractmethod
from typing import List, Dict, Any
import time
import requests
from src.models import Article, FetchSettings
from src.utils.logger import get_logger

logger = get_logger()


class BaseFetcher(ABC):
    """Abstract base class for all news fetchers"""

    def __init__(self, fetch_settings: FetchSettings):
        self.settings = fetch_settings
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': fetch_settings.user_agent
        })

    @abstractmethod
    def fetch(self, source_config: Dict[str, Any]) -> List[Article]:
        """
        Fetch articles from a news source

        Args:
            source_config: Source configuration dictionary

        Returns:
            List of Article objects
        """
        pass

    def _retry_on_failure(self, func, max_retries: int = 3, retry_delay: int = 5):
        """
        Retry a function on failure with exponential backoff

        Args:
            func: Function to retry
            max_retries: Maximum number of retry attempts
            retry_delay: Initial delay between retries in seconds

        Returns:
            Function result

        Raises:
            Last exception if all retries fail
        """
        last_exception = None

        for attempt in range(max_retries):
            try:
                return func()
            except Exception as e:
                last_exception = e
                if attempt < max_retries - 1:
                    delay = retry_delay * (2 ** attempt)  # Exponential backoff
                    logger.warning(
                        f"Attempt {attempt + 1}/{max_retries} failed: {e}. "
                        f"Retrying in {delay} seconds..."
                    )
                    time.sleep(delay)
                else:
                    logger.error(f"All {max_retries} attempts failed")

        raise last_exception

    def _validate_response(self, response: requests.Response) -> bool:
        """
        Validate HTTP response

        Args:
            response: requests.Response object

        Returns:
            True if response is valid

        Raises:
            requests.HTTPError if response is invalid
        """
        response.raise_for_status()
        return True

    def close(self):
        """Close the session"""
        self.session.close()

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
