from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime
from collections import defaultdict
from src.storage.base_storage import BaseStorage
from src.models import Article
from src.utils.logger import get_logger
from src.utils.date_utils import get_today_filename, format_date

logger = get_logger()


class MarkdownStorage(BaseStorage):
    """Markdown file storage backend"""

    def __init__(self, output_dir: str, organize_by_date: bool = True, **kwargs):
        super().__init__(output_dir, **kwargs)
        self.organize_by_date = organize_by_date
        self.output_path = Path(output_dir)
        self.output_path.mkdir(parents=True, exist_ok=True)

    def save(self, articles: List[Article], filename: Optional[str] = None, **kwargs):
        """
        Save articles to Markdown file

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
            tag_str = '_'.join(tags[:2]) if tags else category_clean
            tag_clean = tag_str.replace(' ', '_').replace('/', '_').lower()

            if self.organize_by_date:
                date_str = get_today_filename()
                filename = f"{date_str}_{source_clean}_{tag_clean}"
            else:
                filename = f"{source_clean}_{category_clean}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        file_path = self.output_path / f"{filename}.md"

        # Generate markdown content
        markdown = self._generate_markdown(articles, kwargs.get('source'), kwargs.get('category'))

        # Save to file
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(markdown)

            logger.info(f"Saved {len(articles)} articles to {file_path}")

        except Exception as e:
            logger.error(f"Failed to save markdown: {e}")
            raise

    def load(self, filters: Optional[Dict[str, Any]] = None) -> List[Article]:
        """
        Load articles from Markdown files

        Note: This is a simplified implementation.
        Parsing markdown back to Article objects is not fully supported.

        Args:
            filters: Optional filters

        Returns:
            Empty list (markdown is primarily for export)
        """
        logger.warning("Loading from Markdown is not fully supported")
        return []

    def _generate_markdown(self, articles: List[Article], source: str = None, category: str = None) -> str:
        """
        Generate formatted markdown content

        Args:
            articles: List of articles

        Returns:
            Markdown string
        """
        # Group articles by source and category
        grouped = defaultdict(lambda: defaultdict(list))
        for article in articles:
            grouped[article.source][article.category].append(article)

        # Generate markdown
        lines = []

        # Header
        source_title = f" - {source}" if source else ""
        category_title = f" / {category}" if category else ""
        lines.append(f"# News Summary{source_title}{category_title}")
        lines.append(f"## {format_date(datetime.now(), '%B %d, %Y')}")
        lines.append("")
        lines.append(f"Total articles: {len(articles)}")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Table of Contents
        lines.append("## Table of Contents")
        lines.append("")
        for source in sorted(grouped.keys()):
            lines.append(f"- [{source}](#{source.lower().replace(' ', '-')})")
            for category in sorted(grouped[source].keys()):
                lines.append(f"  - [{category}](#{source.lower().replace(' ', '-')}-{category.lower().replace(' ', '-')})")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Articles by source and category
        for source in sorted(grouped.keys()):
            lines.append(f"## {source}")
            lines.append("")

            for category in sorted(grouped[source].keys()):
                category_articles = grouped[source][category]
                lines.append(f"### {category}")
                lines.append("")

                for article in category_articles:
                    lines.append(f"#### {article.title}")
                    lines.append("")
                    lines.append(f"**Published:** {format_date(article.published_date, '%Y-%m-%d %H:%M')}")
                    lines.append("")
                    lines.append(f"**Link:** [{article.url}]({article.url})")
                    lines.append("")

                    if article.tags:
                        lines.append(f"**Tags:** {', '.join(article.tags)}")
                        lines.append("")

                    # Add full content
                    if article.content:
                        lines.append("**完整内容：**")
                        lines.append("")
                        # Content is already formatted with paragraphs separated by double newlines
                        # Split by double newline to preserve paragraph structure
                        paragraphs = article.content.split('\n\n')
                        for para in paragraphs:
                            para = para.strip()
                            if para:
                                lines.append(para)
                                lines.append("")  # Add blank line after each paragraph

                    # Add summary if available
                    if article.summary:
                        lines.append("**自动摘要：**")
                        lines.append("")
                        lines.append(article.summary)
                        lines.append("")

                    lines.append("---")
                    lines.append("")

        return "\n".join(lines)
