# AutoNews 项目结构完整说明

## 📁 目录树

```
autonews/
├── config/                        # 配置文件
│   ├── config.yaml               # 主配置（调度、存储、处理）
│   ├── sources.yaml              # 新闻源配置
│   └── sources.example.yaml      # 配置示例（所有功能）
│
├── src/                          # 源代码
│   ├── core/                     # 核心模块
│   │   ├── config_manager.py     # 配置管理器
│   │   ├── scheduler.py          # 定时调度器
│   │   ├── notifier.py           # 通知系统
│   │   └── session_manager.py    # 会话管理（认证/代理/Cookie）
│   │
│   ├── fetchers/                 # 抓取器
│   │   ├── base_fetcher.py       # 抽象基类
│   │   ├── rss_fetcher.py        # RSS抓取器
│   │   ├── web_scraper.py        # 网页爬虫
│   │   ├── content_extractor.py  # 内容提取器
│   │   └── factory.py            # 工厂模式
│   │
│   ├── processors/               # 数据处理
│   │   ├── deduplicator.py       # SHA256去重
│   │   ├── summarizer.py         # 摘要生成（sumy）
│   │   └── classifier.py         # 分类器
│   │
│   ├── storage/                  # 存储
│   │   ├── base_storage.py       # 抽象基类
│   │   ├── json_storage.py       # JSON存储
│   │   └── markdown_storage.py   # Markdown导出
│   │
│   ├── tts/                      # 文本转语音
│   │   ├── __init__.py
│   │   └── edge_tts_converter.py # Edge TTS转换器
│   │
│   ├── ai/                       # AI集成 🆕
│   │   ├── __init__.py
│   │   └── openrouter_client.py  # OpenRouter API客户端
│   │
│   ├── models.py                 # 数据模型
│   └── utils/                    # 工具函数
│       ├── logger.py             # 日志工具
│       ├── hash_utils.py         # 哈希工具
│       └── date_utils.py         # 日期工具
│
├── tools/                        # 命令行工具
│   ├── cookie_helper.py          # Cookie管理工具
│   ├── news_to_audio.py          # 单篇文章转音频
│   └── generate_daily_digest.py  # AI摘要生成 🆕
│
├── data/                         # 数据目录
│   ├── processed/                # JSON文件
│   ├── exports/                  # Markdown文件
│   ├── digest/                   # AI摘要 🆕
│   ├── audio/                    # 音频文件
│   ├── cookies/                  # Cookie存储
│   └── history/                  # 去重历史
│
├── docs/                         # 文档
│   ├── COMPLETE_GUIDE.md         # 完整功能指南
│   ├── AUTHENTICATION_GUIDE.md   # 认证配置指南
│   ├── TTS_GUIDE.md              # TTS完整指南
│   ├── TTS_QUICKSTART.md         # TTS快速开始
│   ├── AI_DIGEST_GUIDE.md        # AI摘要指南 🆕
│   ├── AI_QUICKSTART.md          # AI快速开始 🆕
│   ├── RSS_CONTENT_EXTRACTION.md # RSS优化说明
│   ├── NEW_FEATURES.md           # 新功能概述
│   └── PROJECT_STRUCTURE.md      # 本文档
│
├── logs/                         # 日志
│   └── autonews.log
│
├── .env                          # 环境变量（API Key）
├── .env.example                  # 环境变量示例
├── .gitignore                    # Git忽略配置
├── main.py                       # 主程序入口
├── requirements.txt              # Python依赖
├── README.md                     # 项目说明
└── FINAL_SUMMARY.md              # 完整总结 🆕
```

## 📦 核心模块说明

### src/core/ - 核心模块

| 文件 | 功能 | 关键类/函数 |
|------|------|------------|
| `config_manager.py` | 配置管理 | ConfigManager |
| `scheduler.py` | 定时任务 | Scheduler |
| `notifier.py` | 通知系统 | Notifier |
| `session_manager.py` | 会话管理 | SessionManager |

### src/fetchers/ - 抓取器

| 文件 | 功能 | 关键类/函数 |
|------|------|------------|
| `base_fetcher.py` | 抽象基类 | BaseFetcher |
| `rss_fetcher.py` | RSS解析 | RSSFetcher |
| `web_scraper.py` | 网页爬虫 | WebScraper |
| `content_extractor.py` | 内容提取 | ContentExtractor |
| `factory.py` | 工厂模式 | FetcherFactory |

### src/processors/ - 数据处理

| 文件 | 功能 | 关键类/函数 |
|------|------|------------|
| `deduplicator.py` | SHA256去重 | Deduplicator |
| `summarizer.py` | 摘要生成 | Summarizer |
| `classifier.py` | 分类 | Classifier |

### src/storage/ - 存储

| 文件 | 功能 | 关键类/函数 |
|------|------|------------|
| `base_storage.py` | 抽象基类 | BaseStorage |
| `json_storage.py` | JSON存储 | JSONStorage |
| `markdown_storage.py` | Markdown | MarkdownStorage |

### src/tts/ - 文本转语音

| 文件 | 功能 | 关键类/函数 |
|------|------|------------|
| `edge_tts_converter.py` | Edge TTS | EdgeTTSConverter |

### src/ai/ - AI集成 🆕

| 文件 | 功能 | 关键类/函数 |
|------|------|------------|
| `openrouter_client.py` | OpenRouter | OpenRouterClient |

## 🛠️ 工具脚本

| 工具 | 功能 | 使用示例 |
|------|------|----------|
| `cookie_helper.py` | Cookie管理 | `python tools/cookie_helper.py import "36氪" cookies.json` |
| `news_to_audio.py` | 文章转音频 | `python tools/news_to_audio.py --daily` |
| `generate_daily_digest.py` | AI摘要 🆕 | `python tools/generate_daily_digest.py` |

## 📋 配置文件

| 文件 | 说明 |
|------|------|
| `.env` | 环境变量（API Key） |
| `config/config.yaml` | 主配置 |
| `config/sources.yaml` | 新闻源配置 |

## 📊 数据文件

| 目录 | 说明 | 文件格式 |
|------|------|----------|
| `data/processed/` | 原始JSON | `{date}_{source}_{tags}.json` |
| `data/exports/` | Markdown | `{date}_{source}_{tags}.md` |
| `data/digest/` | AI摘要 🆕 | `{date}_digest.txt/mp3` |
| `data/audio/` | 音频文件 | `{date}_{source}_{n}.mp3` |
| `data/cookies/` | Cookie | `{source}.json` |

## 📚 文档

| 文档 | 说明 | 页数 |
|------|------|------|
| `README.md` | 项目概述 | - |
| `FINAL_SUMMARY.md` | 完整总结 | 20+ |
| `docs/COMPLETE_GUIDE.md` | 完整指南 | 40+ |
| `docs/AUTHENTICATION_GUIDE.md` | 认证指南 | 50+ |
| `docs/TTS_GUIDE.md` | TTS指南 | 40+ |
| `docs/AI_DIGEST_GUIDE.md` | AI指南 🆕 | 40+ |

## 🔗 模块依赖关系

```
main.py
  ├── ConfigManager (config_manager.py)
  ├── Scheduler (scheduler.py)
  ├── SessionManager (session_manager.py) 🆕
  ├── Fetchers (fetchers/)
  │   ├── RSSFetcher
  │   ├── WebScraper
  │   └── ContentExtractor
  ├── Processors (processors/)
  │   ├── Deduplicator
  │   └── Summarizer
  └── Storage (storage/)
      ├── JSONStorage
      └── MarkdownStorage

tools/generate_daily_digest.py 🆕
  ├── OpenRouterClient (ai/openrouter_client.py)
  ├── EdgeTTSConverter (tts/edge_tts_converter.py)
  └── JSONStorage (storage/json_storage.py)
```

## 📝 文件命名规范

### 代码文件
- **模块**: `snake_case.py`
- **类**: `PascalCase`
- **函数**: `snake_case()`

### 数据文件
- **JSON**: `{date}_{source}_{tags}.json`
- **Markdown**: `{date}_{source}_{tags}.md`
- **音频**: `{date}_{source}_{n}.mp3`
- **摘要**: `{date}_digest.txt/mp3`

### 示例
```
2026-02-07_36氪_科技_创业.json
2026-02-07_36氪_科技_创业.md
2026-02-07_36氪_01.mp3
2026-02-07_digest.txt
2026-02-07_digest.mp3
```

---

最后更新：2026-02-07
