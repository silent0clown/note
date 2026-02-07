# AutoNews - Quick Start Guide

## 5-Minute Setup

### 1. Install Dependencies (1 minute)

```bash
cd /home/temp/autonews
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Test Run (2 minutes)

```bash
# Run tests
python tests/test_basic.py

# Fetch news once
python main.py --once
```

### 3. Check Results (1 minute)

```bash
# View logs
tail logs/autonews.log

# Check if any articles were saved
ls -lh data/processed/
ls -lh data/exports/

# View deduplication history
cat data/history/hashes.json
```

### 4. Start Scheduled Execution (1 minute)

```bash
# Run with scheduler (Ctrl+C to stop)
python main.py

# Or run in background
nohup python main.py > autonews.out 2>&1 &
```

## Common Tasks

### Change Fetch Schedule

Edit `config/config.yaml`:
```yaml
scheduler:
  cron: "0 */6 * * *"  # Every 6 hours
```

### Add News Source

Edit `config/sources.yaml`:
```yaml
sources:
  - name: "New Source"
    enabled: true
    type: "rss"
    categories:
      - name: "Category"
        url: "https://example.com/rss"
        tags: ["tag1"]
```

### Disable Summarization

Edit `config/config.yaml`:
```yaml
processing:
  summarization:
    enabled: false
```

### View Articles

```bash
# JSON format
cat data/processed/$(date +%Y-%m-%d).json | jq '.'

# Markdown format
cat data/exports/$(date +%Y-%m-%d).md

# Count articles
cat data/processed/$(date +%Y-%m-%d).json | jq '. | length'
```

### Clear History and Re-fetch

```bash
rm data/history/hashes.json
python main.py --once
```

## Troubleshooting

### No articles saved?
- Check network connectivity
- Verify RSS feed URLs are accessible
- Run with `--debug` flag: `python main.py --debug --once`

### Permission errors?
```bash
chmod -R u+w data/ logs/
```

### Dependencies issue?
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

## File Locations

- **Config**: `config/*.yaml`
- **Articles**: `data/processed/*.json`
- **Exports**: `data/exports/*.md`
- **Logs**: `logs/autonews.log`
- **History**: `data/history/hashes.json`

## Command Reference

```bash
python main.py              # Run with scheduler
python main.py --once       # Run once and exit
python main.py --debug      # Enable debug logging
python main.py --help       # Show help
```

## Project Structure

```
autonews/
├── config/           # YAML configuration
├── src/              # Python source code
├── data/             # Saved articles
├── logs/             # Application logs
├── tests/            # Test suite
└── main.py           # Entry point
```

For detailed documentation, see:
- **README.md** - Full project documentation
- **USAGE.md** - Comprehensive usage guide
- **IMPLEMENTATION_SUMMARY.md** - Technical details
