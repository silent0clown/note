# AutoNews TTS (文本转语音) 使用指南

## 概述

AutoNews 集成了 **Edge TTS**，可以将新闻文章转换为高质量的音频文件。

### 为什么选择 Edge TTS？

- ✅ **完全免费** - 无限制调用，无需API Key
- ✅ **零资源占用** - 调用云端API，不占用服务器资源
- ✅ **音质优秀** - 与微软Azure TTS付费版相同
- ✅ **支持中文** - 多种音色（女声、男声、儿童等）
- ✅ **易于使用** - 简单的命令行工具

### 系统要求

- **CPU**: 无特殊要求（仅网络调用）
- **内存**: 无特殊要求（<50MB）
- **硬盘**: 取决于音频文件数量（每篇文章约2-5MB）
- **网络**: 需要连接互联网

---

## 快速开始

### 1. 转换单个JSON文件

将36氪的文章转换为音频：

```bash
source venv/bin/activate
python tools/news_to_audio.py -f data/processed/2026-02-07_36氪_科技_创业.json
```

**输出**:
```
✓ Successfully converted 10/10 articles
```

**生成的文件**:
```
data/audio/
  ├── 2026-02-07_36氪_01.mp3  (4.6 MB)
  ├── 2026-02-07_36氪_02.mp3  (3.2 MB)
  └── ...
```

### 2. 只转换前3篇文章

```bash
python tools/news_to_audio.py -f data/processed/2026-02-07_36氪_科技_创业.json -n 3
```

### 3. 转换今天的所有文章

```bash
python tools/news_to_audio.py --daily
```

会转换所有来源的文章（IT之家、36氪、Solidot等）

### 4. 转换指定日期的文章

```bash
python tools/news_to_audio.py --daily -d 2026-02-07
```

---

## 语音选择

### 可用的中文语音

| 语音ID | 性别 | 特点 | 适用场景 |
|--------|------|------|----------|
| **xiaoxiao** | 女 | 温柔、自然 | 通用（默认） |
| **yunyang** | 男 | 专业、播报感 | 新闻播报 |
| **yunxi** | 男 | 沉稳、磁性 | 深度文章 |
| **yunhao** | 男 | 阳光、活力 | 科技快讯 |
| **xiaomo** | 女 | 甜美、亲切 | 轻松阅读 |
| **xiaochen** | 女 | 温和、舒缓 | 睡前听读 |
| **xiaoyou** | 女童 | 活泼、可爱 | 儿童内容 |

### 使用不同语音

```bash
# 使用男声（新闻播报）
python tools/news_to_audio.py -f file.json --voice yunyang

# 使用女声（甜美）
python tools/news_to_audio.py -f file.json --voice xiaomo

# 使用男声（沉稳）
python tools/news_to_audio.py -f file.json --voice yunxi
```

### 查看所有可用语音

```bash
edge-tts --list-voices | grep zh-CN
```

---

## 语速和音调调整

### 语速调整

```bash
# 正常语速（默认）
python tools/news_to_audio.py -f file.json --rate +0%

# 快速播报（推荐新闻）
python tools/news_to_audio.py -f file.json --rate +15%

# 慢速播报（适合学习）
python tools/news_to_audio.py -f file.json --rate -20%

# 极快速度
python tools/news_to_audio.py -f file.json --rate +50%
```

**取值范围**: -50% 到 +100%

### 推荐语速

- **新闻快讯**: +15% 到 +20%
- **深度文章**: +5% 到 +10%
- **学习材料**: -10% 到 +0%
- **睡前听读**: -20% 到 -10%

---

## 高级用法

### 1. 自定义输出目录

```bash
python tools/news_to_audio.py -f file.json -o /path/to/audio
```

### 2. 批量转换示例

```bash
#!/bin/bash
# 转换今天所有来源的文章，使用不同语音

# IT之家 - 使用男声（阳光）
python tools/news_to_audio.py -f data/processed/2026-02-07_it之家_*.json --voice yunhao --rate +15%

# 36氪 - 使用男声（播报）
python tools/news_to_audio.py -f data/processed/2026-02-07_36氪_*.json --voice yunyang --rate +10%

# Solidot - 使用男声（沉稳）
python tools/news_to_audio.py -f data/processed/2026-02-07_solidot_*.json --voice yunxi --rate +5%
```

### 3. 集成到定时任务

在 `crontab` 中添加：

```cron
# 每天早上8点抓取新闻
0 8 * * * cd /home/temp/autonews && source venv/bin/activate && python main.py --once

# 每天早上8:05转换为音频
5 8 * * * cd /home/temp/autonews && source venv/bin/activate && python tools/news_to_audio.py --daily --voice yunyang --rate +15%
```

---

## Python API 使用

### 简单示例

```python
from src.tts import text_to_speech

# 转换单段文本
text_to_speech(
    text="你好，这是AutoNews自动生成的新闻播报。",
    output_file="data/audio/test.mp3",
    voice="yunyang",
    rate="+15%"
)
```

### 高级示例

```python
from src.tts import EdgeTTSConverter
import asyncio

async def convert_article():
    converter = EdgeTTSConverter(
        voice='yunyang',
        rate='+15%',
        volume='+0%',
        pitch='+0Hz'
    )

    article_text = """
    文章标题：春节AI大战，催生AI应用超级大国

    来源：36氪

    豆包、元宝、文心们还在沿用"发红包"的老套路吸引用户时...
    """

    await converter.convert_text_to_speech(
        text=article_text,
        output_file="data/audio/article.mp3"
    )

asyncio.run(convert_article())
```

### 批量转换

```python
import json
from tools.news_to_audio import NewsToAudioConverter
import asyncio

async def batch_convert():
    converter = NewsToAudioConverter(
        voice='yunyang',
        rate='+15%',
        output_dir='data/audio'
    )

    # 转换JSON文件
    await converter.convert_from_json(
        'data/processed/2026-02-07_36氪_科技_创业.json',
        max_articles=5
    )

asyncio.run(batch_convert())
```

---

## 文件组织

### 默认输出结构

```
data/audio/
├── 2026-02-07_36氪_01.mp3
├── 2026-02-07_36氪_02.mp3
├── 2026-02-07_it之家_01.mp3
├── 2026-02-07_solidot_01.mp3
└── ...
```

### 文件命名规则

格式: `{日期}_{来源}_{序号}.mp3`

例如:
- `2026-02-07_36氪_01.mp3` - 36氪第1篇
- `2026-02-07_hackernews_05.mp3` - HackerNews第5篇

---

## 音频格式说明

### 输出格式

- **格式**: MP3
- **编码**: AAC
- **采样率**: 24kHz
- **比特率**: 48kbps
- **声道**: 单声道（Mono）

### 文件大小估算

- **短文章** (500字): ~0.5-1 MB
- **中等文章** (2000字): ~2-3 MB
- **长文章** (5000字): ~4-6 MB

**示例**:
```
春节AI大战，催生AI应用超级大国 (4998字) -> 4.6 MB
时长: 约6分钟
```

---

## 性能和资源消耗

### 转换速度

- **单篇文章**: 10-60秒（取决于文章长度和网络速度）
- **10篇文章**: 2-5分钟
- **每日50篇**: 10-15分钟

### 资源占用

| 资源 | 占用 |
|------|------|
| CPU | <5% (仅网络传输) |
| 内存 | <50MB |
| 网络 | 约1MB/文章 |
| 硬盘 | 约3MB/文章 |

**2C2G服务器完全够用！** ✅

---

## 常见问题

### Q1: 转换失败怎么办？

**检查网络连接**:
```bash
ping www.microsoft.com
```

**查看日志**:
```bash
tail -f logs/autonews.log
```

**常见错误**:
- `Connection timeout` - 网络问题，重试即可
- `No module named 'edge_tts'` - 运行 `pip install edge-tts`

### Q2: 如何调整音频质量？

Edge TTS的音质是固定的（24kHz, 48kbps），这是微软Azure的标准。如果需要更高质量，可以考虑：
1. 使用付费的Azure TTS（支持48kHz）
2. 使用本地TTS模型（如Piper）

但对于新闻播报，当前质量已经很好。

### Q3: 可以离线使用吗？

Edge TTS需要网络连接。如果需要完全离线，建议使用：
- **Piper TTS** (轻量级，100MB模型)
- **Coqui TTS** (音质更好，但需要更多资源)

### Q4: 支持其他语言吗？

支持！Edge TTS支持100+种语言和方言：

```bash
# 英语
--voice en-US-JennyNeural

# 日语
--voice ja-JP-NanamiNeural

# 韩语
--voice ko-KR-SunHiNeural

# 粤语
--voice zh-HK-HiuGaaiNeural

# 台湾话
--voice zh-TW-HsiaoChenNeural
```

查看所有语音:
```bash
edge-tts --list-voices
```

### Q5: 如何合并多个音频文件？

使用 `ffmpeg`:

```bash
# 安装ffmpeg
apt-get install ffmpeg

# 创建文件列表
cat > filelist.txt << EOF
file '2026-02-07_36氪_01.mp3'
file '2026-02-07_36氪_02.mp3'
file '2026-02-07_36氪_03.mp3'
EOF

# 合并
ffmpeg -f concat -safe 0 -i filelist.txt -c copy output.mp3
```

### Q6: 能否在线播放？

可以！将音频文件放到Web服务器：

```bash
# 启动简单的HTTP服务器
cd data/audio
python3 -m http.server 8080

# 访问
http://your-server:8080/2026-02-07_36氪_01.mp3
```

或使用Nginx/Apache托管。

---

## 播客和RSS Feed

### 创建播客Feed

可以为音频生成RSS feed，让用户订阅：

```python
# 示例代码（需要自己实现）
# 生成podcast.xml
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
  <channel>
    <title>AutoNews 每日播报</title>
    <description>科技新闻自动播报</description>
    <item>
      <title>2026-02-07 36氪科技新闻</title>
      <enclosure url="http://example.com/audio/2026-02-07_36氪_01.mp3"
                 type="audio/mpeg"
                 length="4816384"/>
      <pubDate>Fri, 07 Feb 2026 08:00:00 GMT</pubDate>
    </item>
  </channel>
</rss>
```

---

## 最佳实践

### 1. 新闻播报推荐配置

```bash
# 使用专业男声，语速稍快
python tools/news_to_audio.py \
    --daily \
    --voice yunyang \
    --rate +15%
```

### 2. 深度阅读推荐配置

```bash
# 使用温柔女声，正常语速
python tools/news_to_audio.py \
    --daily \
    --voice xiaoxiao \
    --rate +5%
```

### 3. 通勤听新闻

```bash
# 转换前5篇，快速播报
python tools/news_to_audio.py \
    -f data/processed/2026-02-07_36氪_*.json \
    -n 5 \
    --voice yunhao \
    --rate +20%
```

### 4. 睡前听新闻

```bash
# 慢速、舒缓
python tools/news_to_audio.py \
    --daily \
    --voice xiaochen \
    --rate -15%
```

---

## 自动化工作流

### 完整的自动化流程

```bash
#!/bin/bash
# auto_news_audio.sh - 每日自动新闻播报

cd /home/temp/autonews
source venv/bin/activate

# 1. 抓取新闻
echo "📰 Fetching news..."
python main.py --once

# 2. 转换为音频
echo "🎙️ Converting to audio..."
python tools/news_to_audio.py --daily --voice yunyang --rate +15%

# 3. 清理7天前的音频
echo "🗑️ Cleaning old audio..."
find data/audio -name "*.mp3" -mtime +7 -delete

# 4. 生成播放列表
echo "📋 Generating playlist..."
ls data/audio/*.mp3 > data/audio/playlist.txt

echo "✅ Done!"
```

添加到crontab:
```cron
0 8 * * * /home/temp/autonews/auto_news_audio.sh >> /var/log/autonews_auto.log 2>&1
```

---

## 故障排除

### 问题：转换速度很慢

**原因**: 网络速度慢

**解决**:
1. 检查网络连接
2. 减少并发转换数量
3. 考虑在网络好的时间段运行

### 问题：音频中有杂音

**原因**: Edge TTS服务端问题（极少见）

**解决**:
1. 重新转换
2. 尝试不同的语音
3. 检查原文本是否有特殊字符

### 问题：某些文章转换失败

**原因**: 文本太长或包含特殊字符

**解决**:
```python
# 限制文本长度
text = text[:10000]  # 最多10000字符

# 清理特殊字符
import re
text = re.sub(r'[^\w\s\u4e00-\u9fff。，！？、；：""''（）《》【】]', '', text)
```

---

## 总结

Edge TTS 为 AutoNews 提供了：

✅ **完全免费** - 永久免费，无限制
✅ **高音质** - 专业级TTS
✅ **低资源** - 2C2G完全够用
✅ **易使用** - 一行命令搞定
✅ **多语音** - 10+种中文音色

**开始使用**:
```bash
python tools/news_to_audio.py --daily --voice yunyang --rate +15%
```

**享受您的自动化新闻播报！** 🎊

---

**相关文档**:
- [Edge TTS 官方文档](https://github.com/rany2/edge-tts)
- [微软 Azure TTS](https://azure.microsoft.com/services/cognitive-services/text-to-speech/)

**更新日期**: 2026-02-07
