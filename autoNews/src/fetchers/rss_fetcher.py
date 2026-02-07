import feedparser
from typing import List, Dict, Any
from datetime import datetime
from src.fetchers.base_fetcher import BaseFetcher
from src.models import Article, FetchSettings
from src.utils.logger import get_logger
from src.utils.date_utils import parse_date, parse_struct_time

logger = get_logger()


class RSSFetcher(BaseFetcher):
    """Fetcher for RSS/Atom feeds"""

    def __init__(self, fetch_settings: FetchSettings):
        super().__init__(fetch_settings)

    def fetch(self, source_config: Dict[str, Any]) -> List[Article]:
        """
        Fetch articles from RSS feed

        Args:
            source_config: Source configuration containing:
                - name: Source name (e.g., "BBC")
                - categories: List of category configs with url and tags

        Returns:
            List of Article objects
        """
        articles = []
        source_name = source_config.get('name', 'Unknown')

        for category in source_config.get('categories', []):
            category_name = category.get('name', 'Unknown')
            feed_url = category.get('url')
            tags = category.get('tags', [])

            if not feed_url:
                logger.warning(f"No URL for {source_name}/{category_name}")
                continue

            try:
                category_articles = self._fetch_feed(
                    feed_url,
                    source_name,
                    category_name,
                    tags
                )
                articles.extend(category_articles)
                logger.info(
                    f"Fetched {len(category_articles)} articles from "
                    f"{source_name}/{category_name}"
                )

            except Exception as e:
                logger.error(
                    f"Failed to fetch {source_name}/{category_name}: {e}"
                )

        return articles

    def _fetch_feed(
        self,
        url: str,
        source: str,
        category: str,
        tags: List[str]
    ) -> List[Article]:
        """
        Fetch and parse a single RSS feed

        Args:
            url: Feed URL
            source: Source name
            category: Category name
            tags: List of tags to apply

        Returns:
            List of Article objects
        """
        def fetch_func():
            # Use custom headers
            response = self.session.get(
                url,
                timeout=self.settings.timeout
            )
            self._validate_response(response)
            return response.content

        # Retry on failure
        content = self._retry_on_failure(fetch_func)

        # Parse feed
        feed = feedparser.parse(content)

        # Check for parsing errors
        if feed.bozo:
            logger.warning(
                f"Feed parsing warning for {url}: {feed.bozo_exception}"
            )

        articles = []
        max_articles = self.settings.max_articles_per_source

        for entry in feed.entries[:max_articles]:
            try:
                article = self._parse_entry(entry, source, category, tags)
                articles.append(article)
            except Exception as e:
                logger.warning(f"Failed to parse entry: {e}")
                continue

        return articles

    def _parse_entry(
        self,
        entry: feedparser.FeedParserDict,
        source: str,
        category: str,
        tags: List[str]
    ) -> Article:
        """
        Parse a feed entry into an Article object

        Args:
            entry: feedparser entry
            source: Source name
            category: Category name
            tags: List of tags

        Returns:
            Article object
        """
        # Extract title
        title = entry.get('title', '').strip()

        # Extract URL
        url = entry.get('link', '').strip()

        # Extract published date
        published_date = None
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            published_date = parse_struct_time(entry.published_parsed)
        elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
            published_date = parse_struct_time(entry.updated_parsed)
        elif hasattr(entry, 'published'):
            published_date = parse_date(entry.published)
        else:
            published_date = datetime.now()

        # Extract content
        content = None
        if self.settings.include_content:
            # Try multiple content fields
            if hasattr(entry, 'content') and entry.content:
                content = entry.content[0].get('value', '')
            elif hasattr(entry, 'summary'):
                content = entry.summary
            elif hasattr(entry, 'description'):
                content = entry.description

            # Clean HTML tags if needed (basic cleaning)
            if content:
                content = self._clean_html(content)

        # Create article
        article = Article(
            title=title,
            url=url,
            source=source,
            category=category,
            published_date=published_date,
            content=content,
            tags=tags.copy() if tags else []
        )

        return article

    def _clean_html(self, html: str) -> str:
        """
        Clean HTML and extract meaningful text content

        For feeds like 36Kr that include full HTML in CDATA,
        this properly extracts and formats the text content.

        Args:
            html: HTML string

        Returns:
            Cleaned plain text with proper paragraph formatting
        """
        try:
            from bs4 import BeautifulSoup

            # Parse HTML
            soup = BeautifulSoup(html, 'lxml')

            # Remove script, style, and other non-content elements
            for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside', 'iframe']):
                element.decompose()

            # Extract paragraphs and headings
            paragraphs = []

            # Get all text-containing elements in order
            for element in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'div']):
                text = element.get_text(separator=' ', strip=True)

                # Skip empty or very short fragments
                if not text or len(text) < 10:
                    continue

                # Skip if it's just whitespace
                if not text.strip():
                    continue

                paragraphs.append(text)

            # If we got good paragraphs, join them
            if paragraphs:
                # Remove duplicates while preserving order
                seen = set()
                unique_paragraphs = []
                for p in paragraphs:
                    if p not in seen:
                        seen.add(p)
                        unique_paragraphs.append(p)

                return '\n\n'.join(unique_paragraphs)

            # Fallback: get all text
            return soup.get_text(separator='\n', strip=True)

        except Exception as e:
            logger.warning(f"HTML cleaning failed: {e}")
            # Fallback: return as-is
            return html
