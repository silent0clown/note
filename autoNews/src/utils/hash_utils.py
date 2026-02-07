import hashlib
from src.models import Article


def compute_article_hash(article: Article) -> str:
    """
    Compute a unique hash for an article based on title, URL, and published date

    This helps detect duplicate articles even if they are fetched from different sources
    or at different times.

    Args:
        article: Article object to hash

    Returns:
        SHA256 hash string
    """
    # Combine key identifying fields
    content = f"{article.title}|{article.url}|{article.published_date.isoformat()}"

    # Compute SHA256 hash
    return hashlib.sha256(content.encode('utf-8')).hexdigest()


def compute_content_hash(content: str) -> str:
    """
    Compute hash for arbitrary content

    Args:
        content: String content to hash

    Returns:
        SHA256 hash string
    """
    return hashlib.sha256(content.encode('utf-8')).hexdigest()
