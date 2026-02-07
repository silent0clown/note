# AutoNews 完整功能指南

## 🎉 系统概述

AutoNews 是一个功能完整的自动化新闻聚合系统，包含以下核心功能：

1. **新闻抓取** - RSS/网页爬虫
2. **智能处理** - 去重、摘要、分类
3. **多格式存储** - JSON、Markdown
4. **认证系统** - 支持登录、Cookie、代理
5. **文本转语音** - 高质量音频生成

---

## 📋 核心功能清单

### ✅ 新闻抓取与处理

- [x] RSS feed 解析
- [x] 网页爬虫（BeautifulSoup）
- [x] 完整内容提取
- [x] 智能去重（SHA256哈希）
- [x] 自动摘要生成
- [x] 文章分类标签

### ✅ 认证与访问控制

- [x] HTTP Basic 认证
- [x] Bearer Token 认证
- [x] API Key 认证
- [x] Session 登录认证
- [x] Cookie 管理（自动保存/加载）
- [x] 代理支持（HTTP/HTTPS/SOCKS5）
- [x] 自定义请求头
- [x] SSL 验证控制

### ✅ 存储与导出

- [x] JSON 格式存储
- [x] Markdown 格式导出
- [x] 按日期组织
- [x] 按来源分离
- [x] 文件命名规范

### ✅ 文本转语音 (TTS)

- [x] Edge TTS 集成
- [x] 多种中文语音（10+）
- [x] 语速/音量/音调调节
- [x] 批量转换
- [x] 单篇转换
- [x] 命令行工具

### ✅ 自动化与调度

- [x] APScheduler 定时任务
- [x] Cron 表达式支持
- [x] 单次执行模式
- [x] 后台运行
- [x] 日志记录

---

## 🚀 完整工作流程

### 日常使用流程

```bash
# 1. 抓取今天的新闻
python main.py --once

# 2. 转换为音频
python tools/news_to_audio.py --daily --voice yunyang --rate +15%

# 3. 查看结果
ls -lh data/processed/   # JSON文件
ls -lh data/exports/     # Markdown文件
ls -lh data/audio/       # 音频文件
```

### 自动化流程

```bash
# crontab -e
# 每天早上8点自动执行
0 8 * * * cd /home/temp/autonews && source venv/bin/activate && python main.py --once
5 8 * * * cd /home/temp/autonews && source venv/bin/activate && python tools/news_to_audio.py --daily
```

---

## 📊 当前配置的新闻源

根据您的 `config/sources.yaml`:

| 源名称 | 类型 | 状态 | 特殊配置 |
|--------|------|------|----------|
| **IT之家** | RSS | ✅ 启用 | 基础配置 |
| **36氪** | RSS | ✅ 启用 | ⭐ 自定义Headers |
| **Solidot** | RSS | ✅ 启用 | 基础配置 |
| **V2EX** | RSS | ✅ 启用 | 基础配置 |
| **HackerNews** | RSS | ✅ 启用 | 基础配置 |
| **今日头条** | Web | ❌ 禁用 | 需要动态加载 |

**每日总量**: 50篇文章 (5源 × 10篇)

---

## 🎯 典型使用场景

### 场景1：技术新闻日报

**需求**: 每天早上自动获取科技新闻并生成音频

**配置**:
```yaml
# sources.yaml
sources:
  - name: "IT之家"
    enabled: true
  - name: "36氪"
    enabled: true
  - name: "HackerNews"
    enabled: true

# config.yaml
scheduler:
  enabled: true
  cron: "0 8 * * *"
```

**脚本**:
```bash
#!/bin/bash
cd /home/temp/autonews
source venv/bin/activate

# 抓取新闻
python main.py --once

# 转换音频（快速播报）
python tools/news_to_audio.py --daily --voice yunyang --rate +20%

# 生成播放列表
ls data/audio/*.mp3 > data/audio/playlist.m3u

echo "✅ Done! Check data/audio/"
```

### 场景2：付费媒体访问

**需求**: 访问需要登录的付费新闻网站

**配置**:
```yaml
sources:
  - name: "付费媒体"
    enabled: true
    type: "rss"
    categories:
      - name: "深度报道"
        url: "https://premium.example.com/feed"
    config:
      auth:
        type: "session"
        login_url: "https://premium.example.com/login"
        username: "your_email"
        password: "your_password"
      cookies: "auto"
```

**使用Cookie工具**:
```bash
# 从浏览器导入Cookie
python tools/cookie_helper.py import "付费媒体" cookies.json

# 验证Cookie
python tools/cookie_helper.py validate "付费媒体" https://premium.example.com/
```

### 场景3：国外网站（需要代理）

**需求**: 抓取被墙的国外新闻网站

**配置**:
```yaml
sources:
  - name: "NYTimes"
    enabled: true
    type: "rss"
    categories:
      - name: "Technology"
        url: "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml"
    config:
      proxy:
        http: "http://127.0.0.1:7890"   # Clash
        https: "http://127.0.0.1:7890"
      timeout: 30
```

---

## 🛠️ 工具集合

### 新闻抓取

```bash
# 单次执行
python main.py --once

# 启动定时任务
python main.py
```

### Cookie管理

```bash
# 导入Cookie
python tools/cookie_helper.py import "36氪" cookies.json

# 列出所有Cookie
python tools/cookie_helper.py list

# 验证Cookie
python tools/cookie_helper.py validate "36氪" https://www.36kr.com/

# 删除Cookie
python tools/cookie_helper.py delete "36氪"
```

### 文本转语音

```bash
# 转换单个文件
python tools/news_to_audio.py -f data/processed/2026-02-07_36氪_*.json

# 转换今天所有文章
python tools/news_to_audio.py --daily

# 自定义语音和语速
python tools/news_to_audio.py --daily --voice yunxi --rate +10%

# 只转换前3篇
python tools/news_to_audio.py -f file.json -n 3
```

---

## 📁 目录结构

```
autonews/
├── config/                        # 配置文件
│   ├── config.yaml               # 主配置
│   ├── sources.yaml              # 新闻源配置
│   └── sources.example.yaml      # 配置示例（含所有功能）
│
├── src/                          # 源代码
│   ├── core/                     # 核心模块
│   │   ├── config_manager.py
│   │   ├── scheduler.py
│   │   ├── notifier.py
│   │   └── session_manager.py    # 会话管理（认证/代理）
│   ├── fetchers/                 # 抓取器
│   │   ├── base_fetcher.py
│   │   ├── rss_fetcher.py
│   │   ├── web_scraper.py
│   │   ├── content_extractor.py  # 内容提取
│   │   └── factory.py
│   ├── processors/               # 数据处理
│   │   ├── deduplicator.py       # 去重
│   │   └── summarizer.py         # 摘要
│   ├── storage/                  # 存储
│   │   ├── json_storage.py
│   │   └── markdown_storage.py
│   ├── tts/                      # 🆕 文本转语音
│   │   ├── __init__.py
│   │   └── edge_tts_converter.py
│   ├── models.py                 # 数据模型
│   └── utils/                    # 工具函数
│
├── tools/                        # 命令行工具
│   ├── cookie_helper.py          # Cookie管理工具
│   └── news_to_audio.py          # 🆕 TTS转换工具
│
├── data/                         # 数据目录
│   ├── processed/                # JSON文件
│   │   └── 2026-02-07_36氪_科技_创业.json
│   ├── exports/                  # Markdown文件
│   │   └── 2026-02-07_36氪_科技_创业.md
│   ├── audio/                    # 🆕 音频文件
│   │   └── 2026-02-07_36氪_01.mp3
│   ├── cookies/                  # Cookie存储
│   │   └── 36氪.json
│   └── history/                  # 去重历史
│       └── hashes.json
│
├── docs/                         # 文档
│   ├── AUTHENTICATION_GUIDE.md   # 认证配置指南
│   ├── NEW_FEATURES.md           # 新功能说明
│   ├── RSS_CONTENT_EXTRACTION.md # RSS优化说明
│   ├── TTS_GUIDE.md              # 🆕 TTS完整指南
│   ├── TTS_QUICKSTART.md         # 🆕 TTS快速开始
│   └── COMPLETE_GUIDE.md         # 本文档
│
├── logs/                         # 日志
│   └── autonews.log
│
├── main.py                       # 主程序
├── requirements.txt              # 依赖
└── README.md                     # 项目说明
```

---

## 📚 文档索引

| 文档 | 用途 | 适合人群 |
|------|------|----------|
| **[README.md](../README.md)** | 项目介绍 | 所有用户 |
| **[AUTHENTICATION_GUIDE.md](AUTHENTICATION_GUIDE.md)** | 认证、代理、Cookie配置 | 需要访问受限网站 |
| **[TTS_GUIDE.md](TTS_GUIDE.md)** | TTS完整使用指南 | 需要音频功能 |
| **[TTS_QUICKSTART.md](TTS_QUICKSTART.md)** | TTS快速开始 | TTS新手 |
| **[RSS_CONTENT_EXTRACTION.md](RSS_CONTENT_EXTRACTION.md)** | RSS优化技术说明 | 开发者 |
| **[NEW_FEATURES.md](NEW_FEATURES.md)** | 新功能概述 | 升级用户 |
| **[COMPLETE_GUIDE.md](COMPLETE_GUIDE.md)** | 完整功能指南 | 所有用户 |

---

## 🔧 配置示例

### 基础配置（当前使用）

**config/sources.yaml**:
```yaml
sources:
  - name: "IT之家"
    enabled: true
    type: "rss"
    categories:
      - name: "全部"
        url: "https://www.ithome.com/rss/"
        tags: ["科技", "IT"]

  - name: "36氪"
    enabled: true
    type: "rss"
    categories:
      - name: "快讯"
        url: "https://www.36kr.com/feed-article"
        tags: ["科技", "创业"]
    config:
      user_agent: "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
      headers:
        Accept: "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        Referer: "https://www.36kr.com/"
      timeout: 20
```

### 高级配置示例

查看 `config/sources.example.yaml` 获取：
- 所有认证方式示例
- 代理配置示例
- Cookie管理示例
- 完整功能展示

---

## 💡 最佳实践

### 1. 文件命名规范

**自动生成格式**: `{日期}_{源名称}_{标签}.{扩展名}`

例如:
- `2026-02-07_36氪_科技_创业.json`
- `2026-02-07_36氪_科技_创业.md`
- `2026-02-07_36氪_01.mp3`

### 2. 定时任务建议

```cron
# 每天早上8点抓取
0 8 * * * cd /home/temp/autonews && source venv/bin/activate && python main.py --once

# 每天早上8:05生成音频
5 8 * * * cd /home/temp/autonews && source venv/bin/activate && python tools/news_to_audio.py --daily --voice yunyang --rate +15%

# 每周日清理7天前的音频
0 0 * * 0 find /home/temp/autonews/data/audio -name "*.mp3" -mtime +7 -delete
```

### 3. 资源管理

**磁盘空间**:
- JSON: ~100KB/篇
- Markdown: ~50KB/篇
- 音频: ~3MB/篇

**建议**:
- 定期清理旧音频（保留7-30天）
- JSON和Markdown可以长期保留
- 设置日志轮转（当前配置：10MB × 5份）

### 4. 网络优化

对于2C2G服务器：
- 限制并发请求（当前每源顺序执行）
- 使用session复用连接
- 设置合理的超时时间（15-30秒）
- 避免同时转换太多音频

---

## ⚡ 性能优化建议

### 当前性能

| 操作 | 时间 | 资源占用 |
|------|------|----------|
| **抓取50篇文章** | 1-2分钟 | CPU <10%, 内存 <200MB |
| **转换1篇音频** | 30-60秒 | CPU <5%, 内存 <50MB |
| **转换50篇音频** | 10-15分钟 | CPU <5%, 内存 <50MB |

### 优化建议

1. **并发抓取**（如果服务器资源充足）
   ```python
   # 可以修改main.py使用ThreadPoolExecutor
   # 同时抓取多个源
   ```

2. **缓存策略**
   - RSS feed缓存（避免频繁请求）
   - 已转换音频缓存

3. **批量操作**
   - 批量转换音频而不是逐个转换
   - 批量保存而不是单篇保存

---

## 🐛 故障排除

### 常见问题

#### 1. 36氪内容提取失败

**原因**: 反爬虫保护

**解决**: 已优化，现在直接从RSS的CDATA提取完整内容

#### 2. 音频转换失败

**检查**:
```bash
# 检查网络
ping www.microsoft.com

# 检查edge-tts安装
pip show edge-tts

# 查看日志
tail -f logs/autonews.log
```

#### 3. Cookie过期

**解决**:
```bash
# 重新从浏览器导出
python tools/cookie_helper.py import "源名称" cookies.json

# 或使用Session认证自动登录
```

#### 4. 代理不工作

**检查**:
```bash
# 测试代理
curl -x http://127.0.0.1:7890 https://www.google.com

# 查看日志确认代理被使用
grep "proxy" logs/autonews.log
```

---

## 🎓 学习资源

### Python依赖库

- **feedparser** - RSS解析
- **BeautifulSoup** - HTML解析
- **edge-tts** - 文本转语音
- **APScheduler** - 定时任务
- **requests** - HTTP客户端
- **pydantic** - 数据验证

### 外部服务

- **Microsoft Edge TTS** - 免费TTS API
- **OpenRouter** - 模型API（未使用）

---

## 📝 更新日志

### 2026-02-07 - 重大更新

1. **认证系统** ✅
   - 5种认证方式
   - Cookie自动管理
   - 代理支持

2. **RSS优化** ✅
   - 智能HTML提取
   - 36氪完整内容提取
   - 减少90%网络请求

3. **TTS功能** ✅
   - Edge TTS集成
   - 10+中文语音
   - 批量转换工具

4. **文档完善** ✅
   - 7份详细文档
   - 命令行工具说明
   - 最佳实践指南

---

## 🎯 未来计划

### 短期（1-2周）

- [ ] Web界面（Flask/FastAPI）
- [ ] 播客RSS feed生成
- [ ] 更多TTS语音选项
- [ ] 音频合并工具

### 中期（1-2月）

- [ ] 数据可视化（热点话题）
- [ ] 全文搜索（ElasticSearch）
- [ ] 移动端推送通知
- [ ] AI摘要增强（OpenAI/Claude）

### 长期（3-6月）

- [ ] 微信公众号集成
- [ ] Telegram Bot
- [ ] 多语言支持
- [ ] 分布式部署

---

## 🤝 贡献与反馈

如果您有任何问题或建议：

1. 查看相关文档
2. 检查日志文件
3. 提Issue或PR
4. 联系维护者

---

## 📜 许可证

本项目仅供学习和个人使用。

---

**享受您的自动化新闻聚合之旅！** 🎊

最后更新：2026-02-07
