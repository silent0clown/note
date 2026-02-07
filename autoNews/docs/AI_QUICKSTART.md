# AI新闻摘要 - 快速开始

## 🚀 5分钟上手

### 1. 配置API Key

```bash
# 创建.env文件
echo "OPENROUTER_API_KEY=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" > .env
```

### 2. 生成AI新闻摘要

```bash
cd /home/temp/autonews
source venv/bin/activate

# 先抓取新闻（如果还没抓）
python main.py --once

# 生成AI摘要（文本+音频）
python tools/generate_daily_digest.py
```

**输出**:
- `data/digest/2026-02-07_digest.txt` (1.8KB)
- `data/digest/2026-02-07_digest.mp3` (786KB)

---

## 📋 常用命令

### 基础用法

```bash
# 今天的摘要
python tools/generate_daily_digest.py

# 指定日期
python tools/generate_daily_digest.py -d 2026-02-07

# 只要文本，不要音频
python tools/generate_daily_digest.py --no-audio
```

### 自定义风格

```bash
# 专业风格（默认）
python tools/generate_daily_digest.py --style 专业

# 轻松风格
python tools/generate_daily_digest.py --style 轻松

# 简洁风格（要点式）
python tools/generate_daily_digest.py --style 简洁
```

### 控制长度

```bash
# 短摘要（500字）
python tools/generate_daily_digest.py --max-length 500

# 长摘要（2000字）
python tools/generate_daily_digest.py --max-length 2000
```

---

## 🎯 完整工作流

```bash
#!/bin/bash
# daily_ai_news.sh

cd /home/temp/autonews
source venv/bin/activate

# 1. 抓取新闻
python main.py --once

# 2. 生成AI摘要
python tools/generate_daily_digest.py

echo "✅ 完成！查看结果："
ls -lh data/digest/
```

**添加到crontab**:
```cron
0 8 * * * ~/daily_ai_news.sh >> /var/log/autonews.log 2>&1
```

---

## 🤖 免费AI模型

**默认**: `tngtech/deepseek-r1t2-chimera:free` ⭐推荐

**其他选择**:
```bash
python tools/generate_daily_digest.py --model meta-llama/llama-3.2-3b-instruct:free
python tools/generate_daily_digest.py --model microsoft/phi-3-mini-128k-instruct:free
```

---

## 📖 详细文档

[完整AI摘要指南](AI_DIGEST_GUIDE.md)

---

## 💡 工作流对比

### 之前：50篇独立文章

```
data/processed/
├── 2026-02-07_it之家_*.json (10篇)
├── 2026-02-07_36氪_*.json (10篇)
├── 2026-02-07_solidot_*.json (10篇)
├── 2026-02-07_v2ex_*.json (10篇)
└── 2026-02-07_hackernews_*.json (10篇)
```

### 现在：1份AI精炼摘要

```
data/digest/
├── 2026-02-07_digest.txt (核心要点)
└── 2026-02-07_digest.mp3 (语音播报)
```

**时间对比**:
- 阅读50篇文章：约2小时
- 阅读AI摘要：5分钟
- 听音频摘要：3分钟

---

**享受AI驱动的智能新闻！** 🎊
