# AutoNews - Automated News Aggregation Tool

AutoNews is a Python-based automated news aggregation tool that fetches articles from configurable news sources (like BBC, CNN, etc.), processes them, and stores them locally in various formats.

## Features

### Core Features
- **Multi-source Support**: Configure multiple news sources (RSS/Atom feeds)
- **Category-based Fetching**: Organize articles by category (Technology, Science, Arts, etc.)
- **Smart Deduplication**: Avoid fetching duplicate articles using content hashing
- **Automatic Summarization**: Generate summaries using extractive summarization
- **Multiple Storage Formats**: Save articles as JSON, Markdown, or CSV
- **Scheduled Execution**: Automatic daily fetching using cron-like scheduling
- **Flexible Configuration**: YAML-based configuration for easy customization
- **Comprehensive Logging**: Detailed logging with rotation support

### 🆕 Advanced Features (New!)
- **Universal Authentication**: Support for HTTP Basic, Bearer Token, API Key, Session-based, and custom authentication
- **Cookie Management**: Automatic cookie loading/saving, browser cookie import support
- **Proxy Support**: HTTP/HTTPS/SOCKS5 proxies with authentication
- **Per-Source Configuration**: Each source can have independent auth, proxy, and headers
- **Full Content Extraction**: Intelligent extraction of complete article content from original URLs
- **Anti-Scraping Protection**: Customizable User-Agent and headers to bypass website restrictions

### 🎙️ Text-to-Speech (TTS)
- **Edge TTS Integration**: Convert articles to high-quality audio using Microsoft Edge TTS
- **Completely Free**: No API key required, unlimited usage
- **Multiple Voices**: 10+ Chinese voices (male, female, child)
- **Low Resource**: Works perfectly on 2C2G servers
- **Batch Conversion**: Convert entire daily digest to audio
- **Customizable**: Adjust speed, pitch, and voice

### 🤖 AI-Powered Digest (New!)
- **OpenRouter Integration**: Use free AI models to summarize news
- **Intelligent Analysis**: Automatically extract key points from all sources
- **Multiple Styles**: Professional, casual, or concise
- **Daily Digest**: Generate one comprehensive news brief from 50+ articles
- **Auto Audio**: Convert AI-generated digest to speech
- **Free Models**: DeepSeek R1, Llama 3.2, and more

📖 **[Authentication Guide →](docs/AUTHENTICATION_GUIDE.md)** | **[TTS Guide →](docs/TTS_GUIDE.md)** | **[AI Digest Guide →](docs/AI_DIGEST_GUIDE.md)**

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone or download this repository:
```bash
cd /home/temp/autonews
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

### Main Configuration (`config/config.yaml`)

Configure the application behavior:

```yaml
scheduler:
  enabled: true
  cron: "0 8 * * *"  # Daily at 8:00 AM

storage:
  type: "json"
  formats:
    - json
    - markdown

processing:
  deduplication:
    enabled: true
  summarization:
    enabled: true
    max_length: 200
```

### News Sources (`config/sources.yaml`)

Configure news sources and categories:

```yaml
sources:
  - name: "BBC"
    enabled: true
    type: "rss"
    categories:
      - name: "Technology"
        url: "http://feeds.bbci.co.uk/news/technology/rss.xml"
        tags: ["tech", "innovation"]
      - name: "Science"
        url: "http://feeds.bbci.co.uk/news/science_and_environment/rss.xml"
        tags: ["science", "environment"]
```

## Usage

### Run Once (Manual Execution)

Fetch articles once and exit:

```bash
python main.py --once
```

### Run with Scheduler

Start the scheduler for automatic periodic fetching:

```bash
python main.py
```

The scheduler will:
1. Run an initial fetch immediately
2. Schedule future fetches based on the cron expression in config
3. Continue running until stopped with Ctrl+C

### Command Line Options

```bash
python main.py --help

Options:
  --config-dir TEXT  Configuration directory path (default: config)
  --once             Run once and exit (no scheduling)
  --debug            Enable debug logging
  --help             Show this message and exit
```

## Output

### JSON Storage

Articles are saved to `data/processed/YYYY-MM-DD.json`:

```json
[
  {
    "title": "Article Title",
    "url": "https://example.com/article",
    "source": "BBC",
    "category": "Technology",
    "published_date": "2026-02-07T10:30:00",
    "content": "Full article content...",
    "summary": "Article summary...",
    "tags": ["tech", "innovation"],
    "hash": "a1b2c3..."
  }
]
```

### Markdown Export

Formatted reports are saved to `data/exports/YYYY-MM-DD.md`:

```markdown
# News Summary - February 07, 2026

## BBC

### Technology

#### Article Title

**Published:** 2026-02-07 10:30

**Link:** [https://example.com/article](https://example.com/article)

**Summary:** Article summary...
```

### Logs

Application logs are saved to `logs/autonews.log` with automatic rotation.

## Project Structure

```
autonews/
├── config/                 # Configuration files
│   ├── config.yaml         # Main configuration
│   └── sources.yaml        # News sources configuration
├── src/
│   ├── core/               # Core modules
│   │   ├── config_manager.py
│   │   ├── scheduler.py
│   │   └── notifier.py
│   ├── fetchers/           # Article fetchers
│   │   ├── base_fetcher.py
│   │   ├── rss_fetcher.py
│   │   └── factory.py
│   ├── processors/         # Data processors
│   │   ├── deduplicator.py
│   │   └── summarizer.py
│   ├── storage/            # Storage backends
│   │   ├── json_storage.py
│   │   └── markdown_storage.py
│   ├── utils/              # Utility functions
│   └── models.py           # Data models
├── data/                   # Data directory
│   ├── processed/          # JSON articles
│   ├── exports/            # Markdown exports
│   └── history/            # Deduplication history
├── logs/                   # Application logs
├── main.py                 # Entry point
├── requirements.txt        # Dependencies
└── README.md
```

## Advanced Usage

### Custom Cron Schedules

Edit `config/config.yaml` to change the schedule:

```yaml
scheduler:
  cron: "0 */6 * * *"  # Every 6 hours
  # cron: "0 9,18 * * *"  # 9 AM and 6 PM daily
  # cron: "0 8 * * 1-5"  # 8 AM on weekdays
```

### Adding New Sources

Add to `config/sources.yaml`:

```yaml
sources:
  - name: "The Guardian"
    enabled: true
    type: "rss"
    categories:
      - name: "Technology"
        url: "https://www.theguardian.com/technology/rss"
        tags: ["tech"]
```

### Disable Summarization

To save processing time, disable summarization in `config/config.yaml`:

```yaml
processing:
  summarization:
    enabled: false
```

## Troubleshooting

### No articles fetched

1. Check internet connection
2. Verify RSS feed URLs are accessible
3. Check logs in `logs/autonews.log`
4. Try running with `--debug` flag

### Permission errors

Ensure write permissions for:
- `data/` directory
- `logs/` directory

### Dependencies installation fails

Try upgrading pip:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Development

### Running Tests

```bash
pytest tests/
```

### Adding New Fetchers

1. Create a new fetcher class inheriting from `BaseFetcher`
2. Implement the `fetch()` method
3. Register it in `FetcherFactory`

## License

This project is provided as-is for educational and personal use.

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## Future Enhancements

- Web scraper for non-RSS sources
- Email notifications
- Web interface for browsing articles
- AI-powered summarization using OpenAI/Claude
- Full-text search capabilities
- Docker containerization
- Database storage option (SQLite/PostgreSQL)

## Support

For issues and questions, please check the logs first and ensure your configuration is valid.
