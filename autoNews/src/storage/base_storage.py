from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from src.models import Article


class BaseStorage(ABC):
    """Abstract base class for storage backends"""

    def __init__(self, output_dir: str, **kwargs):
        self.output_dir = output_dir
        self.config = kwargs

    @abstractmethod
    def save(self, articles: List[Article], **kwargs):
        """
        Save articles to storage

        Args:
            articles: List of Article objects to save
            **kwargs: Additional storage-specific parameters
        """
        pass

    @abstractmethod
    def load(self, filters: Optional[Dict[str, Any]] = None) -> List[Article]:
        """
        Load articles from storage

        Args:
            filters: Optional filters to apply when loading

        Returns:
            List of Article objects
        """
        pass

    def validate_articles(self, articles: List[Article]) -> bool:
        """
        Validate articles before saving

        Args:
            articles: List of articles to validate

        Returns:
            True if valid
        """
        if not articles:
            return False

        for article in articles:
            if not article.title or not article.url:
                return False

        return True
