# AI驱动的新闻摘要指南

## 🤖 功能概述

AutoNews 现在集成了 AI 能力，可以：

1. **智能总结** - 自动分析所有新闻源的内容
2. **生成摘要稿** - 提炼核心要点，生成专业新闻稿
3. **语音播报** - 将摘要稿转换为高质量音频

**核心优势**:
- ✅ **完全免费** - 使用OpenRouter免费模型
- ✅ **智能提炼** - AI自动识别重点新闻
- ✅ **多种风格** - 专业、轻松、简洁可选
- ✅ **即时生成** - 几十秒内完成分析和生成

---

## 🚀 快速开始

### 1分钟：生成今天的AI新闻摘要

```bash
cd /home/temp/autonews
source venv/bin/activate

# 生成摘要（文本+音频）
python tools/generate_daily_digest.py
```

**输出**:
- `data/digest/2026-02-07_digest.txt` - 文本摘要
- `data/digest/2026-02-07_digest.mp3` - 音频播报

---

## 📋 配置说明

### 环境变量设置

**文件**: `.env`

```bash
# OpenRouter API Key (必需)
OPENROUTER_API_KEY=sk-or-v1-your-key-here

# AI模型（可选，默认使用免费模型）
AI_MODEL=tngtech/deepseek-r1t2-chimera:free

# 超时时间（可选，默认120秒）
AI_TIMEOUT=120
```

### 获取 API Key

1. 访问 https://openrouter.ai/
2. 注册/登录账号
3. 进入 Keys 页面
4. 创建新的 API Key
5. 复制到 `.env` 文件

**免费额度**:
- 每天都有免费调用额度
- 足够生成每日新闻摘要

---

## 🎯 使用示例

### 基础使用

```bash
# 生成今天的摘要
python tools/generate_daily_digest.py

# 生成指定日期的摘要
python tools/generate_daily_digest.py -d 2026-02-07

# 只生成文本，不生成音频
python tools/generate_daily_digest.py --no-audio
```

### 自定义风格

```bash
# 专业风格（默认）- 正式、严谨
python tools/generate_daily_digest.py --style 专业

# 轻松风格 - 亲切、口语化
python tools/generate_daily_digest.py --style 轻松

# 简洁风格 - 极简、要点式
python tools/generate_daily_digest.py --style 简洁
```

### 控制长度

```bash
# 短摘要（500字）
python tools/generate_daily_digest.py --max-length 500

# 中摘要（1000字，默认）
python tools/generate_daily_digest.py --max-length 1000

# 长摘要（2000字）
python tools/generate_daily_digest.py --max-length 2000
```

---

## 🤖 可用的免费AI模型

### 推荐模型

| 模型 | 特点 | 适用场景 |
|------|------|----------|
| **tngtech/deepseek-r1t2-chimera:free** ⭐ | 快速、准确 | 新闻摘要（默认） |
| **meta-llama/llama-3.2-3b-instruct:free** | 平衡性好 | 通用摘要 |
| **microsoft/phi-3-mini-128k-instruct:free** | 长文本 | 深度分析 |
| **google/gemma-2-9b-it:free** | 质量高 | 专业摘要 |

### 切换模型

```bash
# 方法1: 使用环境变量
export AI_MODEL=meta-llama/llama-3.2-3b-instruct:free
python tools/generate_daily_digest.py

# 方法2: 使用命令行参数
python tools/generate_daily_digest.py --model meta-llama/llama-3.2-3b-instruct:free
```

### 查看所有免费模型

访问: https://openrouter.ai/models?pricing=free

---

## 📖 工作流程

### 完整的自动化流程

```bash
#!/bin/bash
# daily_news_workflow.sh

cd /home/temp/autonews
source venv/bin/activate

echo "📰 Step 1: 抓取新闻..."
python main.py --once

echo "🤖 Step 2: 生成AI摘要..."
python tools/generate_daily_digest.py

echo "✅ 完成！查看结果："
echo "  文本: data/digest/$(date +%Y-%m-%d)_digest.txt"
echo "  音频: data/digest/$(date +%Y-%m-%d)_digest.mp3"
```

**添加到crontab**:
```cron
# 每天早上8点执行完整流程
0 8 * * * /home/temp/autonews/daily_news_workflow.sh >> /var/log/autonews_workflow.log 2>&1
```

---

## 📊 输出格式

### 文本摘要示例

```
今日新闻摘要

各位听众，早上好！今天是2026年2月7日，以下是今日科技要闻：

核心要点：

1. **AI技术突破** - 阶跃星辰发布Step 3.5 Flash模型，在OpenRouter全球趋势榜
   登顶第一。该模型采用稀疏混合专家架构，性能提升显著。

2. **春节AI大战** - 阿里千问推出"30亿大免单"活动，用AI重塑生活消费场景，
   引领AI应用新趋势。

3. **游戏行业动态** - 2025年游戏行业呈现小年大增长态势，独立游戏和移动游戏
   成为新的增长点。

4. **全键盘手机回归** - 雷火、泰坦等品牌推出全键盘手机，但市场反响平淡，
   昔日黑莓用户已不再买账。

5. **技术社区讨论** - V2EX社区热议全键盘手机话题，反映出怀旧情怀与实用性
   之间的矛盾。

趋势观察：
AI技术正在从工具效率革新向生活方式重塑转变，中国在AI应用领域展现出强大
的创新能力。同时，技术怀旧潮流虽有市场，但难以撼动主流趋势。

以上是今天的新闻摘要，感谢收听。
```

### 音频输出

- **格式**: MP3
- **长度**: 约3-5分钟（取决于摘要长度）
- **文件大小**: 约2-4MB
- **语音**: 专业男声（yunyang）
- **语速**: +10%（适合新闻播报）

---

## 🎨 风格对比

### 专业风格

```
今日科技要闻摘要：

一、AI模型技术突破
阶跃星辰发布Step 3.5 Flash模型，采用稀疏混合专家（MoE）架构...

二、企业战略布局
阿里巴巴推出"春节30亿大免单"活动，旨在通过AI重塑消费场景...
```

### 轻松风格

```
早上好！今天的科技新闻很有意思哦～

首先，有个叫Step 3.5 Flash的AI模型火了，两天就冲到了全球第一！
厉害的是，它不仅聪明，还跑得超级快...

然后呢，阿里这次真的下血本了，直接拿出30亿请全国人民喝奶茶...
```

### 简洁风格

```
今日要点：

• Step 3.5 Flash登顶OpenRouter趋势榜
• 阿里千问30亿大免单活动启动
• 2025游戏行业小年大增长
• 全键盘手机回归反响平淡
• V2EX社区热议科技话题
```

---

## ⚙️ 高级配置

### Python API使用

```python
from src.ai import OpenRouterClient
import asyncio

async def generate_custom_digest():
    # 初始化客户端
    client = OpenRouterClient(
        api_key="sk-or-v1-...",
        model="tngtech/deepseek-r1t2-chimera:free"
    )

    # 加载文章
    import json
    with open('data/processed/2026-02-07_36氪_科技_创业.json') as f:
        articles = json.load(f)

    # 生成摘要
    digest = client.generate_news_digest(
        articles,
        style="轻松",
        max_length=500
    )

    print(digest)

asyncio.run(generate_custom_digest())
```

### 自定义提示词

修改 `src/ai/openrouter_client.py` 中的 `generate_news_digest` 方法：

```python
prompt = f"""你是一位资深新闻编辑，请基于以下新闻，撰写一份{style}的摘要。

自定义要求：
- 重点关注AI和技术创新
- 突出中国企业的进展
- 语言简洁明了

新闻文章：
{combined_text}

请生成摘要："""
```

---

## 📊 性能和成本

### 处理时间

| 操作 | 时间 |
|------|------|
| **加载50篇文章** | 1-2秒 |
| **AI生成摘要** | 10-30秒 |
| **转换为音频** | 20-40秒 |
| **总计** | 约1分钟 |

### API成本

**OpenRouter免费模型**:
- ✅ 完全免费
- ✅ 每天有足够的免费额度
- ✅ 无需信用卡

**付费模型**（可选）:
- GPT-4: ~$0.01/次
- Claude: ~$0.015/次

---

## 🐛 故障排除

### 常见问题

#### 1. API Key错误

**错误信息**:
```
OpenRouter API Key not found
```

**解决**:
```bash
# 检查.env文件
cat .env | grep OPENROUTER_API_KEY

# 确保API Key正确
echo "OPENROUTER_API_KEY=sk-or-v1-..." > .env
```

#### 2. 模型不可用

**错误信息**:
```
Model not found
```

**解决**:
```bash
# 使用默认免费模型
python tools/generate_daily_digest.py

# 或指定其他免费模型
python tools/generate_daily_digest.py --model meta-llama/llama-3.2-3b-instruct:free
```

#### 3. 超时错误

**错误信息**:
```
Request timeout
```

**解决**:
```bash
# 增加超时时间
export AI_TIMEOUT=180
python tools/generate_daily_digest.py
```

#### 4. 没有文章

**错误信息**:
```
No articles found for date: 2026-02-07
```

**解决**:
```bash
# 先抓取新闻
python main.py --once

# 再生成摘要
python tools/generate_daily_digest.py
```

---

## 💡 最佳实践

### 1. 每日自动化

```bash
# 创建自动化脚本
cat > ~/autonews_auto.sh << 'EOF'
#!/bin/bash
cd /home/temp/autonews
source venv/bin/activate

# 抓取新闻
python main.py --once

# 等待3秒
sleep 3

# 生成AI摘要
python tools/generate_daily_digest.py --style 专业 --max-length 800

echo "✅ 完成！"
EOF

chmod +x ~/autonews_auto.sh

# 添加到crontab
echo "0 8 * * * ~/autonews_auto.sh >> /var/log/autonews.log 2>&1" | crontab -
```

### 2. 多风格输出

```bash
# 生成不同风格的摘要
python tools/generate_daily_digest.py --style 专业 --max-length 1000
python tools/generate_daily_digest.py --style 轻松 --max-length 800 --no-audio
python tools/generate_daily_digest.py --style 简洁 --max-length 500 --no-audio
```

### 3. 清理旧文件

```bash
# 清理30天前的摘要
find data/digest -name "*.txt" -mtime +30 -delete
find data/digest -name "*.mp3" -mtime +30 -delete
```

---

## 🎓 技术细节

### AI模型选择标准

1. **速度** - DeepSeek R1 系列（推荐）
2. **质量** - Gemma 2, Llama 3.2
3. **长文本** - Phi-3 Mini (128k context)

### 提示词工程

**核心要素**:
1. 角色设定（资深新闻编辑）
2. 任务描述（撰写摘要稿）
3. 具体要求（风格、长度、结构）
4. 输入内容（新闻文章）

**优化建议**:
- 提供示例输出
- 强调重点关注领域
- 指定输出格式

---

## 🚀 未来规划

### 短期（1-2周）

- [ ] 支持更多AI模型
- [ ] 多语言摘要（英文、日文）
- [ ] 主题分类摘要
- [ ] 可视化报告生成

### 中期（1-2月）

- [ ] 个性化推荐
- [ ] 情感分析
- [ ] 热点趋势预测
- [ ] 多人播报（对话形式）

### 长期（3-6月）

- [ ] 实时新闻摘要
- [ ] 多媒体内容生成（视频、图片）
- [ ] 知识图谱构建
- [ ] 交互式问答

---

## 📝 更新日志

### 2026-02-07 - 初始版本

- ✅ OpenRouter API集成
- ✅ AI新闻摘要生成
- ✅ 多种风格支持
- ✅ TTS集成
- ✅ 命令行工具

---

## 🤝 反馈与支持

如有问题或建议：
1. 查看本文档
2. 检查 `.env` 配置
3. 查看日志 `logs/autonews.log`

---

**享受AI驱动的智能新闻摘要！** 🎊

最后更新：2026-02-07
