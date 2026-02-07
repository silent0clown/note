"""
Web scraper for fetching news from HTML pages
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any
from datetime import datetime
from src.fetchers.base_fetcher import BaseFetcher
from src.models import Article, FetchSettings
from src.utils.logger import get_logger
from src.utils.date_utils import parse_date

logger = get_logger()


class WebScraper(BaseFetcher):
    """Fetcher for scraping news from web pages"""

    def __init__(self, fetch_settings: FetchSettings):
        super().__init__(fetch_settings)

    def fetch(self, source_config: Dict[str, Any]) -> List[Article]:
        """
        Fetch articles by scraping web pages

        Args:
            source_config: Source configuration containing:
                - name: Source name (e.g., "Xinhua")
                - categories: List of category configs with:
                  - url: Page URL to scrape
                  - selectors: CSS selectors for article elements
                  - tags: Tags to apply

        Returns:
            List of Article objects
        """
        articles = []
        source_name = source_config.get('name', 'Unknown')

        for category in source_config.get('categories', []):
            category_name = category.get('name', 'Unknown')
            page_url = category.get('url')
            selectors = category.get('selectors', {})
            tags = category.get('tags', [])

            if not page_url:
                logger.warning(f"No URL for {source_name}/{category_name}")
                continue

            try:
                category_articles = self._scrape_page(
                    page_url,
                    source_name,
                    category_name,
                    selectors,
                    tags
                )
                articles.extend(category_articles)
                logger.info(
                    f"Scraped {len(category_articles)} articles from "
                    f"{source_name}/{category_name}"
                )

            except Exception as e:
                logger.error(
                    f"Failed to scrape {source_name}/{category_name}: {e}"
                )

        return articles

    def _scrape_page(
        self,
        url: str,
        source: str,
        category: str,
        selectors: Dict[str, str],
        tags: List[str]
    ) -> List[Article]:
        """
        Scrape a single web page for articles

        Args:
            url: Page URL
            source: Source name
            category: Category name
            selectors: CSS selectors for different elements
            tags: List of tags to apply

        Returns:
            List of Article objects
        """
        def fetch_func():
            response = self.session.get(
                url,
                timeout=self.settings.timeout,
                headers={'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'}
            )
            self._validate_response(response)
            return response

        # Retry on failure
        response = self._retry_on_failure(fetch_func)

        # Parse HTML
        soup = BeautifulSoup(response.content, 'lxml')

        # Get selectors with defaults
        article_selector = selectors.get('article', 'article')
        title_selector = selectors.get('title', 'h2, h3, .title')
        link_selector = selectors.get('link', 'a')
        date_selector = selectors.get('date', 'time, .date, .time')
        summary_selector = selectors.get('summary', 'p, .summary, .description')

        # Find all article elements
        article_elements = soup.select(article_selector)

        if not article_elements:
            logger.warning(f"No articles found with selector '{article_selector}'")
            # Fallback: try common patterns
            article_elements = self._find_articles_fallback(soup)

        articles = []
        max_articles = self.settings.max_articles_per_source

        for elem in article_elements[:max_articles]:
            try:
                article = self._parse_article_element(
                    elem,
                    source,
                    category,
                    tags,
                    url,
                    title_selector,
                    link_selector,
                    date_selector,
                    summary_selector
                )
                if article:
                    articles.append(article)
            except Exception as e:
                logger.debug(f"Failed to parse article element: {e}")
                continue

        return articles

    def _find_articles_fallback(self, soup: BeautifulSoup) -> List:
        """
        Fallback method to find articles using common patterns

        Args:
            soup: BeautifulSoup object

        Returns:
            List of article elements
        """
        # Try common article containers
        for selector in [
            'article',
            '.article',
            '.news-item',
            '.post',
            'li.item',
            'div[class*="item"]',
            'div[class*="article"]',
            'div[class*="news"]'
        ]:
            elements = soup.select(selector)
            if elements:
                logger.info(f"Found articles using fallback selector: {selector}")
                return elements

        return []

    def _parse_article_element(
        self,
        elem,
        source: str,
        category: str,
        tags: List[str],
        base_url: str,
        title_selector: str,
        link_selector: str,
        date_selector: str,
        summary_selector: str
    ) -> Article:
        """
        Parse a single article element

        Args:
            elem: BeautifulSoup element
            source: Source name
            category: Category name
            tags: Tags to apply
            base_url: Base URL for resolving relative links
            title_selector: CSS selector for title
            link_selector: CSS selector for link
            date_selector: CSS selector for date
            summary_selector: CSS selector for summary

        Returns:
            Article object or None
        """
        # Extract title
        title_elem = elem.select_one(title_selector)
        if not title_elem:
            return None
        title = title_elem.get_text(strip=True)

        if not title:
            return None

        # Extract link
        link_elem = elem.select_one(link_selector)
        if not link_elem:
            return None

        url = link_elem.get('href', '')
        if not url:
            return None

        # Resolve relative URLs
        if url.startswith('/'):
            from urllib.parse import urljoin
            url = urljoin(base_url, url)
        elif not url.startswith('http'):
            return None

        # Extract date
        date_elem = elem.select_one(date_selector)
        if date_elem:
            date_text = date_elem.get_text(strip=True)
            # Try to get datetime attribute first
            date_attr = date_elem.get('datetime') or date_elem.get('data-time')
            published_date = parse_date(date_attr or date_text)
        else:
            published_date = datetime.now()

        # Extract summary/content
        content = None
        if self.settings.include_content:
            summary_elem = elem.select_one(summary_selector)
            if summary_elem:
                content = summary_elem.get_text(strip=True)

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


class XinhuaScraper(WebScraper):
    """
    Specialized scraper for Xinhua News (新华网)
    """

    def _scrape_page(
        self,
        url: str,
        source: str,
        category: str,
        selectors: Dict[str, str],
        tags: List[str]
    ) -> List[Article]:
        """Scrape Xinhua news page"""

        def fetch_func():
            response = self.session.get(
                url,
                timeout=self.settings.timeout,
                headers={
                    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                    'Accept': 'text/html,application/xhtml+xml'
                }
            )
            self._validate_response(response)
            return response

        response = self._retry_on_failure(fetch_func)

        # Xinhua uses GB2312 or UTF-8 encoding
        if 'charset=gb2312' in response.text.lower() or 'charset=gbk' in response.text.lower():
            response.encoding = 'gb2312'
        else:
            response.encoding = 'utf-8'

        soup = BeautifulSoup(response.content, 'lxml')

        articles = []

        # Xinhua specific selectors
        # Try multiple patterns as Xinhua's structure varies
        article_patterns = [
            'ul.dataList li',           # Common list pattern
            'div.box01 ul li',          # News list box
            'div.newsList ul li',       # News list
            'div[class*="list"] li',    # Generic list
            'li[class*="item"]',        # List items
        ]

        article_elements = []
        for pattern in article_patterns:
            elements = soup.select(pattern)
            if elements and len(elements) > 3:  # Need at least a few articles
                article_elements = elements
                logger.info(f"Found {len(elements)} articles with pattern: {pattern}")
                break

        if not article_elements:
            logger.warning("No articles found on Xinhua page")
            return articles

        max_articles = self.settings.max_articles_per_source

        for elem in article_elements[:max_articles]:
            try:
                # Find link
                link_elem = elem.find('a')
                if not link_elem:
                    continue

                # Extract title
                title = link_elem.get_text(strip=True)
                if not title or len(title) < 5:
                    continue

                # Extract URL
                article_url = link_elem.get('href', '')
                if not article_url:
                    continue

                # Resolve relative URLs
                if article_url.startswith('/'):
                    from urllib.parse import urljoin
                    article_url = urljoin(url, article_url)
                elif not article_url.startswith('http'):
                    continue

                # Extract date - Xinhua usually has a span with date
                date_elem = elem.find('span', class_=lambda x: x and ('time' in x.lower() or 'date' in x.lower()))
                if not date_elem:
                    date_elem = elem.find('span')

                if date_elem:
                    date_text = date_elem.get_text(strip=True)
                    published_date = self._parse_xinhua_date(date_text)
                else:
                    published_date = datetime.now()

                # Create article
                article = Article(
                    title=title,
                    url=article_url,
                    source=source,
                    category=category,
                    published_date=published_date,
                    tags=tags.copy() if tags else []
                )

                articles.append(article)

            except Exception as e:
                logger.debug(f"Failed to parse Xinhua article: {e}")
                continue

        return articles

    def _parse_xinhua_date(self, date_text: str) -> datetime:
        """
        Parse Xinhua date formats
        Common formats: "2026-02-07", "02-07 14:30", "14:30"
        """
        import re

        # Remove extra whitespace
        date_text = date_text.strip()

        # Pattern: YYYY-MM-DD HH:MM:SS or YYYY-MM-DD
        if re.match(r'\d{4}-\d{2}-\d{2}', date_text):
            return parse_date(date_text)

        # Pattern: MM-DD HH:MM (assume current year)
        match = re.match(r'(\d{2})-(\d{2})\s+(\d{2}):(\d{2})', date_text)
        if match:
            month, day, hour, minute = match.groups()
            current_year = datetime.now().year
            return datetime(current_year, int(month), int(day), int(hour), int(minute))

        # Pattern: MM-DD (assume current year)
        match = re.match(r'(\d{2})-(\d{2})', date_text)
        if match:
            month, day = match.groups()
            current_year = datetime.now().year
            return datetime(current_year, int(month), int(day))

        # Pattern: HH:MM (assume today)
        match = re.match(r'(\d{2}):(\d{2})', date_text)
        if match:
            hour, minute = match.groups()
            now = datetime.now()
            return datetime(now.year, now.month, now.day, int(hour), int(minute))

        # Fallback
        return datetime.now()
