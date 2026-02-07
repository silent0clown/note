# TTS 快速开始 - 5分钟上手

## 🚀 最快速度上手

### 1分钟：转换单个文件

```bash
cd /home/temp/autonews
source venv/bin/activate
python tools/news_to_audio.py -f data/processed/2026-02-07_36氪_科技_创业.json -n 1
```

**结果**: 生成 `data/audio/2026-02-07_36氪_01.mp3` (约4.6MB)

---

## 📋 常用命令

### 转换今天所有文章

```bash
python tools/news_to_audio.py --daily
```

### 转换单个来源（前5篇）

```bash
python tools/news_to_audio.py -f data/processed/2026-02-07_36氪_*.json -n 5
```

### 使用专业男声，快速播报

```bash
python tools/news_to_audio.py --daily --voice yunyang --rate +15%
```

---

## 🎤 推荐语音配置

| 场景 | 命令 |
|------|------|
| **新闻播报** | `--voice yunyang --rate +15%` |
| **深度阅读** | `--voice xiaoxiao --rate +5%` |
| **通勤听** | `--voice yunhao --rate +20%` |
| **睡前听** | `--voice xiaochen --rate -15%` |

---

## 🎯 可用语音

```
xiaoxiao  - 女声，温柔（默认）
yunyang   - 男声，新闻播报 ⭐推荐
yunxi     - 男声，沉稳
yunhao    - 男声，阳光
xiaomo    - 女声，甜美
xiaochen  - 女声，舒缓
```

---

## 💡 提示

- **文件位置**: `data/audio/*.mp3`
- **文件大小**: 约3MB/篇（5000字）
- **转换速度**: 约30秒/篇
- **资源占用**: CPU <5%, 内存 <50MB

---

## 📖 详细文档

[完整TTS使用指南](TTS_GUIDE.md)
