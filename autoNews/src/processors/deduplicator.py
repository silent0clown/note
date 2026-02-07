import json
from pathlib import Path
from typing import Set
from src.models import Article
from src.utils.hash_utils import compute_article_hash
from src.utils.logger import get_logger

logger = get_logger()


class Deduplicator:
    """Handles article deduplication using content hashing"""

    def __init__(self, history_file: str):
        self.history_file = Path(history_file)
        self.hashes: Set[str] = set()
        self._load_history()

    def _load_history(self):
        """Load hash history from file"""
        if not self.history_file.exists():
            logger.info("No existing hash history found, starting fresh")
            self.history_file.parent.mkdir(parents=True, exist_ok=True)
            self.hashes = set()
            return

        try:
            with open(self.history_file, 'r') as f:
                data = json.load(f)
                self.hashes = set(data.get('hashes', []))
            logger.info(f"Loaded {len(self.hashes)} hashes from history")
        except Exception as e:
            logger.error(f"Failed to load hash history: {e}")
            self.hashes = set()

    def _save_history(self):
        """Save hash history to file"""
        try:
            self.history_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.history_file, 'w') as f:
                json.dump({
                    'hashes': list(self.hashes),
                    'count': len(self.hashes)
                }, f, indent=2)
            logger.debug(f"Saved {len(self.hashes)} hashes to history")
        except Exception as e:
            logger.error(f"Failed to save hash history: {e}")

    def is_duplicate(self, article: Article) -> bool:
        """
        Check if an article is a duplicate

        Args:
            article: Article to check

        Returns:
            True if article is a duplicate
        """
        article_hash = compute_article_hash(article)
        article.hash = article_hash

        is_dup = article_hash in self.hashes

        if is_dup:
            logger.debug(f"Duplicate found: {article.title[:50]}...")

        return is_dup

    def add_to_history(self, article: Article):
        """
        Add an article to the history

        Args:
            article: Article to add
        """
        if not article.hash:
            article.hash = compute_article_hash(article)

        self.hashes.add(article.hash)
        logger.debug(f"Added to history: {article.title[:50]}...")

    def save(self):
        """Save the current hash history to file"""
        self._save_history()

    def clear_history(self):
        """Clear all hash history"""
        self.hashes = set()
        self._save_history()
        logger.info("Hash history cleared")

    def get_stats(self) -> dict:
        """Get deduplication statistics"""
        return {
            'total_hashes': len(self.hashes),
            'history_file': str(self.history_file)
        }
