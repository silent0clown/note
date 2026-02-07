from typing import Dict, Any
from src.fetchers.base_fetcher import BaseFetcher
from src.fetchers.rss_fetcher import RSSFetcher
from src.fetchers.web_scraper import WebScraper, XinhuaScraper
from src.models import FetchSettings
from src.utils.logger import get_logger

logger = get_logger()


class FetcherFactory:
    """Factory for creating fetcher instances"""

    _fetchers: Dict[str, type] = {
        'rss': RSSFetcher,
        'atom': RSSFetcher,  # RSS fetcher handles Atom feeds too
        'web': WebScraper,
        'xinhua': XinhuaScraper,  # Specialized Xinhua scraper
    }

    @classmethod
    def create(cls, source_type: str, fetch_settings: FetchSettings) -> BaseFetcher:
        """
        Create a fetcher instance based on source type

        Args:
            source_type: Type of source ('rss', 'atom', 'web', etc.)
            fetch_settings: Fetch settings object

        Returns:
            Fetcher instance

        Raises:
            ValueError: If source type is not supported
        """
        source_type = source_type.lower()

        fetcher_class = cls._fetchers.get(source_type)
        if not fetcher_class:
            raise ValueError(
                f"Unsupported source type: {source_type}. "
                f"Supported types: {list(cls._fetchers.keys())}"
            )

        logger.debug(f"Creating {source_type} fetcher")
        return fetcher_class(fetch_settings)

    @classmethod
    def register_fetcher(cls, source_type: str, fetcher_class: type):
        """
        Register a new fetcher type

        Args:
            source_type: Type identifier
            fetcher_class: Fetcher class (must inherit from BaseFetcher)
        """
        if not issubclass(fetcher_class, BaseFetcher):
            raise ValueError("Fetcher must inherit from BaseFetcher")

        cls._fetchers[source_type.lower()] = fetcher_class
        logger.info(f"Registered fetcher for type: {source_type}")

    @classmethod
    def list_supported_types(cls) -> list:
        """List all supported fetcher types"""
        return list(cls._fetchers.keys())
