"""
Basic tests for AutoNews functionality
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import datetime
from src.models import Article
from src.utils.hash_utils import compute_article_hash
from src.utils.date_utils import parse_date, format_date


def test_article_creation():
    """Test Article model creation"""
    article = Article(
        title="Test Article",
        url="https://example.com/article",
        source="BBC",
        category="Technology",
        published_date=datetime.now(),
        content="Test content",
        tags=["test"]
    )

    assert article.title == "Test Article"
    assert article.source == "BBC"
    assert article.category == "Technology"
    assert "test" in article.tags
    print("✓ Article creation test passed")


def test_article_hash():
    """Test article hash computation"""
    article1 = Article(
        title="Test Article",
        url="https://example.com/article",
        source="BBC",
        category="Technology",
        published_date=datetime(2026, 2, 7, 10, 30)
    )

    article2 = Article(
        title="Test Article",
        url="https://example.com/article",
        source="CNN",  # Different source
        category="Technology",
        published_date=datetime(2026, 2, 7, 10, 30)
    )

    hash1 = compute_article_hash(article1)
    hash2 = compute_article_hash(article2)

    # Same title, url, and date should produce same hash
    # regardless of source
    assert hash1 == hash2
    assert len(hash1) == 64  # SHA256 hash length
    print("✓ Article hash test passed")


def test_article_serialization():
    """Test article to_dict and from_dict"""
    original = Article(
        title="Test Article",
        url="https://example.com/article",
        source="BBC",
        category="Technology",
        published_date=datetime(2026, 2, 7, 10, 30),
        content="Test content",
        summary="Test summary",
        tags=["test", "tech"]
    )

    # Convert to dict
    article_dict = original.to_dict()

    # Convert back to Article
    restored = Article.from_dict(article_dict)

    assert restored.title == original.title
    assert restored.url == original.url
    assert restored.source == original.source
    assert restored.category == original.category
    assert restored.content == original.content
    assert restored.summary == original.summary
    assert restored.tags == original.tags
    print("✓ Article serialization test passed")


def test_date_parsing():
    """Test date parsing utilities"""
    # Test ISO format
    date_str = "2026-02-07T10:30:00"
    parsed = parse_date(date_str)
    assert parsed.year == 2026
    assert parsed.month == 2
    assert parsed.day == 7

    # Test formatting
    formatted = format_date(parsed)
    assert formatted == "2026-02-07"

    print("✓ Date parsing test passed")


def test_config_loading():
    """Test configuration loading"""
    from src.core.config_manager import ConfigManager

    config = ConfigManager(config_dir="config")

    # Test basic config access
    app_name = config.get('app.name')
    assert app_name == "AutoNews"

    # Test sources
    sources = config.get_sources()
    assert len(sources) > 0
    assert sources[0].name in ["BBC", "CNN"]

    print("✓ Config loading test passed")


if __name__ == "__main__":
    print("\nRunning AutoNews Basic Tests\n" + "=" * 40)

    try:
        test_article_creation()
        test_article_hash()
        test_article_serialization()
        test_date_parsing()
        test_config_loading()

        print("\n" + "=" * 40)
        print("All tests passed! ✓")
        print("=" * 40 + "\n")

    except AssertionError as e:
        print(f"\n✗ Test failed: {e}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}\n")
        sys.exit(1)
