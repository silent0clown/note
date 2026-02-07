#!/usr/bin/env python3
"""
AutoNews - Automated News Aggregation Tool

Main entry point for the application.
"""

import time
import sys
import signal
from pathlib import Path
import click

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.core.config_manager import ConfigManager
from src.core.scheduler import Scheduler
from src.core.notifier import Notifier
from src.core.session_manager import SessionManager
from src.fetchers.factory import FetcherFactory
from src.fetchers.content_extractor import ContentExtractor
from src.processors.deduplicator import Deduplicator
from src.processors.summarizer import Summarizer
from src.storage.json_storage import JSONStorage
from src.storage.markdown_storage import MarkdownStorage
from src.utils.logger import setup_logger, get_logger


# Global scheduler instance for signal handling
scheduler_instance = None


def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    logger = get_logger()
    logger.info("Received shutdown signal, stopping...")

    if scheduler_instance and scheduler_instance.is_running():
        scheduler_instance.stop()

    sys.exit(0)


def create_storage(config: ConfigManager):
    """
    Create storage instances based on configuration

    Args:
        config: Configuration manager

    Returns:
        Dictionary of storage instances by format
    """
    storage_instances = {}

    output_dir = config.get('storage.output_dir')
    exports_dir = config.get('storage.exports_dir')
    organize_by_date = config.get('storage.organize_by_date')

    for fmt in config.get('storage.formats', ['json']):
        if fmt == 'json':
            storage_instances['json'] = JSONStorage(
                output_dir=output_dir,
                organize_by_date=organize_by_date
            )
        elif fmt == 'markdown':
            storage_instances['markdown'] = MarkdownStorage(
                output_dir=exports_dir,
                organize_by_date=organize_by_date
            )

    return storage_instances


def fetch_task(config: ConfigManager, logger):
    """
    Main task to fetch and process articles

    Args:
        config: Configuration manager
        logger: Logger instance
    """
    logger.info("Starting article fetch task...")

    # Initialize components
    dedup_config = config.get('processing.deduplication')
    deduplicator = Deduplicator(
        dedup_config['history_file']
    ) if dedup_config['enabled'] else None

    summ_config = config.get('processing.summarization')
    summarizer = Summarizer(
        max_length=summ_config['max_length'],
        method=summ_config['method']
    ) if summ_config['enabled'] else None

    storage_instances = create_storage(config)
    notifier = Notifier(config.get('notifications'))

    # Initialize session manager for authentication, cookies, and proxies
    session_manager = SessionManager(cookie_dir="data/cookies")

    # Initialize content extractor (will use sessions from session_manager)
    fetch_settings = config.get_fetch_settings()

    # Fetch articles from all sources
    sources = config.get_sources()
    total_new_articles = 0
    total_duplicates = 0

    for source in sources:
        if not source.enabled:
            logger.info(f"Skipping disabled source: {source.name}")
            continue

        try:
            # Get or create session for this source with its config
            source_session_config = {}

            # Merge global fetch settings with source-specific config
            if hasattr(fetch_settings, 'proxy') and fetch_settings.proxy:
                source_session_config['proxy'] = fetch_settings.proxy
            if hasattr(fetch_settings, 'headers') and fetch_settings.headers:
                source_session_config['headers'] = fetch_settings.headers
            source_session_config['user_agent'] = fetch_settings.user_agent
            source_session_config['timeout'] = fetch_settings.timeout

            # Override with source-specific config if available
            if source.config:
                source_session_config.update(source.config)

            # Get session for this source
            source_session = session_manager.get_session(source.name, source_session_config)

            # Create content extractor with source-specific session
            source_extractor = ContentExtractor(
                timeout=source_session_config.get('timeout', fetch_settings.timeout),
                session=source_session
            )

            # Create appropriate fetcher
            fetcher = FetcherFactory.create(source.type, fetch_settings)

            # Fetch articles
            source_dict = {
                'name': source.name,
                'categories': source.categories
            }
            fetched = fetcher.fetch(source_dict)
            logger.info(f"Fetched {len(fetched)} articles from {source.name}")

            # Process articles for this source
            source_new_articles = []
            source_duplicates = 0

            for article in fetched:
                # Check for duplicates
                if deduplicator and deduplicator.is_duplicate(article):
                    source_duplicates += 1
                    continue

                # Extract full content from URL using source-specific extractor
                # But only if the article doesn't already have substantial content from RSS
                if article.url and fetch_settings.include_content:
                    # Check if RSS already provided good content (like 36Kr)
                    has_good_content = article.content and len(article.content) > 200

                    if not has_good_content:
                        try:
                            full_content = source_extractor.extract(article.url)
                            if full_content:
                                article.content = full_content
                                logger.debug(f"Extracted full content for: {article.title[:50]}...")
                        except Exception as e:
                            logger.warning(f"Failed to extract content from {article.url}: {e}")
                    else:
                        logger.debug(f"Using RSS content for: {article.title[:50]}... ({len(article.content)} chars)")

                # Generate summary
                if summarizer and article.content:
                    try:
                        article.summary = summarizer.generate_summary(article.content)
                    except Exception as e:
                        logger.warning(f"Failed to generate summary for '{article.title}': {e}")

                source_new_articles.append(article)

                # Add to deduplication history
                if deduplicator:
                    deduplicator.add_to_history(article)

            # Save articles for this source separately
            if source_new_articles:
                # Get source metadata for filename
                source_metadata = {
                    'source': source.name,
                    'category': source_new_articles[0].category if source_new_articles else '',
                    'tags': source_new_articles[0].tags if source_new_articles else []
                }

                for fmt, storage in storage_instances.items():
                    try:
                        storage.save(source_new_articles, **source_metadata)
                        logger.info(f"Saved {len(source_new_articles)} articles from {source.name} to {fmt} storage")
                    except Exception as e:
                        logger.error(f"Failed to save {source.name} to {fmt} storage: {e}")

            total_new_articles += len(source_new_articles)
            total_duplicates += source_duplicates

        except Exception as e:
            logger.error(f"Failed to process {source.name}: {e}")
            if not config.get('error_handling.continue_on_error'):
                raise

    # Save deduplication history
    if deduplicator:
        deduplicator.save()

    # Clean up sessions
    session_manager.close_all()

    # Send notification
    if total_new_articles > 0:
        message = (
            f"Successfully fetched and saved {total_new_articles} new articles. "
            f"({total_duplicates} duplicates skipped)"
        )
        notifier.notify_success(message)
        logger.info(message)
    else:
        message = f"No new articles found. ({total_duplicates} duplicates skipped)"
        notifier.notify(message)
        logger.info(message)

    return total_new_articles


@click.command()
@click.option('--config-dir', default='config', help='Configuration directory path')
@click.option('--once', is_flag=True, help='Run once and exit (no scheduling)')
@click.option('--debug', is_flag=True, help='Enable debug logging')
def main(config_dir, once, debug):
    """
    AutoNews - Automated News Aggregation Tool

    Fetches news articles from configured sources, processes them,
    and saves to local storage.
    """
    global scheduler_instance

    # Load configuration
    try:
        config = ConfigManager(config_dir=config_dir)
    except Exception as e:
        print(f"Failed to load configuration: {e}")
        sys.exit(1)

    # Setup logging
    log_level = 'DEBUG' if debug else config.get('logging.level', 'INFO')
    logger = setup_logger(
        name='autonews',
        log_file=config.get('logging.file'),
        level=log_level,
        max_bytes=config.get('logging.max_bytes'),
        backup_count=config.get('logging.backup_count')
    )

    logger.info("=" * 60)
    logger.info("AutoNews Starting")
    logger.info("=" * 60)

    # Validate configuration
    if not config.validate():
        logger.error("Configuration validation failed")
        sys.exit(1)

    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Run once or with scheduler
    if once:
        logger.info("Running in single-execution mode")
        try:
            fetch_task(config, logger)
            logger.info("Execution completed successfully")
        except Exception as e:
            logger.error(f"Execution failed: {e}", exc_info=True)
            sys.exit(1)
    else:
        # Start scheduler
        if config.get('scheduler.enabled'):
            scheduler_instance = Scheduler(timezone=config.get('app.timezone'))

            # Create wrapped task to pass config and logger
            def wrapped_task():
                fetch_task(config, logger)

            # Add scheduled job
            cron_expr = config.get('scheduler.cron')
            scheduler_instance.add_job(wrapped_task, cron_expr)

            # Start scheduler
            scheduler_instance.start()
            logger.info(f"Scheduler started with cron: {cron_expr}")
            logger.info("Press Ctrl+C to stop")

            # Run once immediately on startup
            logger.info("Running initial fetch...")
            try:
                fetch_task(config, logger)
            except Exception as e:
                logger.error(f"Initial fetch failed: {e}", exc_info=True)

            # Keep running
            try:
                while True:
                    time.sleep(1)
            except (KeyboardInterrupt, SystemExit):
                logger.info("Shutting down...")
                scheduler_instance.stop()
        else:
            logger.error("Scheduler is disabled in configuration")
            sys.exit(1)

    logger.info("AutoNews stopped")


if __name__ == "__main__":
    main()
