# AutoNews Usage Guide

## Quick Start

### 1. Initial Setup

```bash
# Navigate to the project directory
cd /home/temp/autonews

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Basic Commands

#### Run Once (Manual Fetch)
```bash
python main.py --once
```

This will:
- Fetch articles from all enabled sources
- Remove duplicates
- Generate summaries
- Save to JSON and Markdown formats
- Exit after completion

#### Run with Scheduler
```bash
python main.py
```

This will:
- Run an initial fetch immediately
- Schedule periodic fetches based on cron expression
- Keep running until stopped (Ctrl+C)

#### Debug Mode
```bash
python main.py --debug --once
```

### 3. Configuration Examples

#### Change Fetch Schedule

Edit `config/config.yaml`:

```yaml
scheduler:
  enabled: true
  cron: "0 */6 * * *"  # Every 6 hours
```

Common cron patterns:
- `"0 8 * * *"` - Daily at 8:00 AM
- `"0 */4 * * *"` - Every 4 hours
- `"0 9,18 * * *"` - 9 AM and 6 PM daily
- `"0 8 * * 1-5"` - 8 AM on weekdays
- `"*/30 * * * *"` - Every 30 minutes

#### Add New News Source

Edit `config/sources.yaml`:

```yaml
sources:
  # Existing sources...

  - name: "Reuters"
    enabled: true
    type: "rss"
    categories:
      - name: "Technology"
        url: "https://www.reuters.com/technology/rss"
        tags: ["tech", "news"]
      - name: "Science"
        url: "https://www.reuters.com/science/rss"
        tags: ["science"]
```

#### Disable Summarization

If summarization is too slow or you don't need it:

```yaml
processing:
  summarization:
    enabled: false
```

#### Change Storage Format

Save only as JSON:

```yaml
storage:
  type: "json"
  formats:
    - json  # Remove 'markdown' to disable MD export
```

Or save both:

```yaml
storage:
  formats:
    - json
    - markdown
```

### 4. Viewing Results

#### JSON Output

Articles are saved to `data/processed/YYYY-MM-DD.json`:

```bash
# View today's articles
cat data/processed/$(date +%Y-%m-%d).json | jq '.'

# Count articles
cat data/processed/$(date +%Y-%m-%d).json | jq '. | length'

# Filter by source
cat data/processed/$(date +%Y-%m-%d).json | jq '.[] | select(.source == "BBC")'

# Get article titles
cat data/processed/$(date +%Y-%m-%d).json | jq '.[].title'
```

#### Markdown Export

Formatted reports in `data/exports/YYYY-MM-DD.md`:

```bash
# View today's export
cat data/exports/$(date +%Y-%m-%d).md

# Open in a browser (if using markdown renderer)
pandoc data/exports/$(date +%Y-%m-%d).md -o /tmp/news.html && xdg-open /tmp/news.html
```

#### Logs

Application logs in `logs/autonews.log`:

```bash
# View recent logs
tail -f logs/autonews.log

# Search for errors
grep ERROR logs/autonews.log

# Count fetched articles
grep "Fetched.*articles from" logs/autonews.log
```

### 5. Advanced Usage

#### Custom Config Directory

```bash
python main.py --config-dir /path/to/config --once
```

#### Programmatic Access

```python
from src.core.config_manager import ConfigManager
from src.storage.json_storage import JSONStorage

# Load configuration
config = ConfigManager()

# Load articles
storage = JSONStorage(output_dir="data/processed")
articles = storage.load(filters={'source': 'BBC'})

# Print titles
for article in articles:
    print(f"{article.title} ({article.category})")
```

#### Clear Deduplication History

If you want to re-fetch all articles:

```bash
rm data/history/hashes.json
python main.py --once
```

### 6. Monitoring

#### Check Scheduler Status

When running with scheduler, you'll see:

```
2026-02-07 08:00:00 - autonews - INFO - Scheduler started with cron: 0 8 * * *
2026-02-07 08:00:00 - autonews - INFO - Running initial fetch...
2026-02-07 08:00:15 - autonews - INFO - Successfully fetched and saved 42 new articles
```

#### System Service (Linux)

To run as a background service, create `/etc/systemd/system/autonews.service`:

```ini
[Unit]
Description=AutoNews Article Fetcher
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/home/temp/autonews
ExecStart=/home/temp/autonews/venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl daemon-reload
sudo systemctl enable autonews
sudo systemctl start autonews
sudo systemctl status autonews
```

### 7. Troubleshooting

#### No articles fetched

```bash
# Test network connectivity
curl -I http://feeds.bbci.co.uk/news/technology/rss.xml

# Check RSS feed validity
python main.py --debug --once 2>&1 | grep -A5 "ERROR"
```

#### Permission errors

```bash
# Fix permissions
chmod -R u+w data/ logs/
```

#### Dependency issues

```bash
# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

#### Clear cache and restart

```bash
# Remove Python cache
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null

# Restart application
python main.py --once
```

### 8. Performance Tips

1. **Limit articles per source** - Edit `config/sources.yaml`:
   ```yaml
   fetch_settings:
     max_articles_per_source: 20  # Reduce from 50
   ```

2. **Disable content fetching** - Only fetch titles and links:
   ```yaml
   fetch_settings:
     include_content: false
   ```

3. **Reduce summary length**:
   ```yaml
   processing:
     summarization:
       max_length: 100  # Reduce from 200
   ```

4. **Disable features you don't need**:
   ```yaml
   processing:
     deduplication:
       enabled: false  # If you don't need dedup
     summarization:
       enabled: false  # If you don't need summaries
   ```

### 9. Integration Examples

#### Send to Email (placeholder in code)

Uncomment email notification code in `src/core/notifier.py` and add to config:

```yaml
notifications:
  enabled: true
  channels:
    - type: "email"
      smtp_server: "smtp.gmail.com"
      smtp_port: 587
      from_addr: "your-email@example.com"
      to_addr: "recipient@example.com"
      username: "your-email@example.com"
      password: "your-app-password"
```

#### Webhook Integration

Similar to email, uncomment webhook code and configure:

```yaml
notifications:
  channels:
    - type: "webhook"
      url: "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
```

### 10. Best Practices

1. **Start with `--once`** - Test configuration before enabling scheduler
2. **Monitor logs** - Check logs regularly for errors
3. **Backup data** - Periodically backup `data/history/hashes.json`
4. **Update sources** - RSS feed URLs may change over time
5. **Rate limiting** - Don't set cron too frequently (respect news sources)
6. **Storage management** - Old JSON files can accumulate; consider cleanup script

## Example Workflow

```bash
# Day 1: Setup and test
python main.py --once --debug

# Verify output
ls -lh data/processed/
cat data/processed/$(date +%Y-%m-%d).json | jq '. | length'

# Day 2: Start scheduler
nohup python main.py > autonews.out 2>&1 &

# Monitor
tail -f logs/autonews.log

# Day 3: Check results
cat data/exports/$(date +%Y-%m-%d).md
```

For more details, see the main [README.md](README.md).
