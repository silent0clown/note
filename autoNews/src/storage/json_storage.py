import json
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime
from src.storage.base_storage import BaseStorage
from src.models import Article
from src.utils.logger import get_logger
from src.utils.date_utils import get_today_filename

logger = get_logger()


class JSONStorage(BaseStorage):
    """JSON file storage backend"""

    def __init__(self, output_dir: str, organize_by_date: bool = True, **kwargs):
        super().__init__(output_dir, **kwargs)
        self.organize_by_date = organize_by_date
        self.output_path = Path(output_dir)
        self.output_path.mkdir(parents=True, exist_ok=True)

    def save(self, articles: List[Article], filename: Optional[str] = None, **kwargs):
        """
        Save articles to JSON file

        Args:
            articles: List of articles to save
            filename: Optional custom filename (without extension)
            **kwargs: Additional parameters (source, category for filename generation)
        """
        if not self.validate_articles(articles):
            logger.warning("No valid articles to save")
            return

        # Determine filename
        if not filename:
            # Get source and category from kwargs or first article
            source = kwargs.get('source', articles[0].source if articles else 'unknown')
            category = kwargs.get('category', articles[0].category if articles else 'all')

            # Clean source and category names for filename
            source_clean = source.replace(' ', '_').replace('/', '_').lower()
            category_clean = category.replace(' ', '_').replace('/', '_').lower()

            # Get tags if available
            tags = kwargs.get('tags', articles[0].tags if articles and articles[0].tags else [])
            tag_str = '_'.join(tags[:2]) if tags else category_clean  # Use first 2 tags or category
            tag_clean = tag_str.replace(' ', '_').replace('/', '_').lower()

            if self.organize_by_date:
                date_str = get_today_filename()
                filename = f"{date_str}_{source_clean}_{tag_clean}"
            else:
                filename = f"{source_clean}_{category_clean}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        file_path = self.output_path / f"{filename}.json"

        # Don't load existing articles - each source gets its own file
        # Convert to dictionaries
        articles_data = [article.to_dict() for article in articles]

        # Save to file
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(articles_data, f, indent=2, ensure_ascii=False)

            logger.info(f"Saved {len(articles)} articles to {file_path}")

        except Exception as e:
            logger.error(f"Failed to save articles: {e}")
            raise

    def load(self, filters: Optional[Dict[str, Any]] = None) -> List[Article]:
        """
        Load articles from JSON files

        Args:
            filters: Optional filters (e.g., {'date': '2026-02-07', 'source': 'BBC'})

        Returns:
            List of Article objects
        """
        articles = []

        # If specific date filter, load that file
        if filters and 'date' in filters:
            file_path = self.output_path / f"{filters['date']}.json"
            if file_path.exists():
                articles.extend(self._load_from_file(file_path))
        else:
            # Load all JSON files
            for json_file in self.output_path.glob("*.json"):
                articles.extend(self._load_from_file(json_file))

        # Apply additional filters
        if filters:
            articles = self._apply_filters(articles, filters)

        return articles

    def _load_from_file(self, file_path: Path) -> List[Article]:
        """Load articles from a specific JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            articles = [Article.from_dict(item) for item in data]
            logger.debug(f"Loaded {len(articles)} articles from {file_path}")
            return articles

        except Exception as e:
            logger.error(f"Failed to load {file_path}: {e}")
            return []

    def _apply_filters(self, articles: List[Article], filters: Dict[str, Any]) -> List[Article]:
        """Apply filters to article list"""
        filtered = articles

        if 'source' in filters:
            filtered = [a for a in filtered if a.source == filters['source']]

        if 'category' in filters:
            filtered = [a for a in filtered if a.category == filters['category']]

        if 'tag' in filters:
            filtered = [a for a in filtered if filters['tag'] in a.tags]

        return filtered
