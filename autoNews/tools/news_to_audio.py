#!/usr/bin/env python3
"""
News to Audio Converter - 将新闻文章转换为音频

支持：
- 单篇文章转音频
- 批量转换
- 自定义语音和语速
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import List, Optional

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.tts.edge_tts_converter import EdgeTTSConverter
from src.models import Article
from src.utils.logger import setup_logger, get_logger

setup_logger(level="INFO")
logger = get_logger()


class NewsToAudioConverter:
    """新闻转音频转换器"""

    def __init__(
        self,
        voice: str = 'xiaoxiao',
        rate: str = '+10%',  # 新闻播报建议稍微快一点
        output_dir: str = 'data/audio'
    ):
        """
        初始化转换器

        Args:
            voice: 语音名称
            rate: 语速
            output_dir: 音频输出目录
        """
        self.converter = EdgeTTSConverter(voice=voice, rate=rate)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def prepare_article_text(self, article: dict) -> str:
        """
        准备文章文本（添加标题、来源等信息）

        Args:
            article: 文章字典

        Returns:
            格式化的文本
        """
        parts = []

        # 标题
        title = article.get('title', '')
        if title:
            parts.append(f"文章标题：{title}")
            parts.append("")  # 空行

        # 来源
        source = article.get('source', '')
        category = article.get('category', '')
        if source:
            source_info = f"来源：{source}"
            if category:
                source_info += f"，分类：{category}"
            parts.append(source_info)
            parts.append("")

        # 正文
        content = article.get('content', article.get('summary', ''))
        if content:
            parts.append(content)
        else:
            parts.append("抱歉，该文章没有内容。")

        return "\n".join(parts)

    async def convert_article(
        self,
        article: dict,
        filename: Optional[str] = None
    ) -> Optional[str]:
        """
        转换单篇文章

        Args:
            article: 文章字典
            filename: 输出文件名（可选）

        Returns:
            输出文件路径，失败返回None
        """
        # 生成文件名
        if not filename:
            title = article.get('title', 'untitled')
            # 清理文件名中的非法字符
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_'))
            safe_title = safe_title[:50]  # 限制长度
            filename = f"{safe_title}.mp3"

        output_file = self.output_dir / filename

        # 准备文本
        text = self.prepare_article_text(article)

        # 转换
        logger.info(f"Converting: {article.get('title', 'Untitled')}")

        success = await self.converter.convert_text_to_speech(
            text,
            str(output_file)
        )

        if success:
            logger.info(f"✓ Saved to: {output_file}")
            return str(output_file)
        else:
            logger.error(f"✗ Failed to convert: {article.get('title', 'Untitled')}")
            return None

    async def convert_from_json(
        self,
        json_file: str,
        max_articles: Optional[int] = None
    ) -> List[str]:
        """
        从JSON文件批量转换

        Args:
            json_file: JSON文件路径
            max_articles: 最多转换的文章数（None表示全部）

        Returns:
            成功转换的文件路径列表
        """
        # 读取JSON
        with open(json_file, 'r', encoding='utf-8') as f:
            articles = json.load(f)

        if not articles:
            logger.warning("No articles found in JSON file")
            return []

        # 限制数量
        if max_articles:
            articles = articles[:max_articles]

        logger.info(f"Converting {len(articles)} articles from {json_file}")

        # 批量转换
        output_files = []

        for i, article in enumerate(articles, 1):
            # 生成带索引的文件名
            source = article.get('source', 'unknown').replace(' ', '_')
            date = article.get('published_date', '').split('T')[0]
            filename = f"{date}_{source}_{i:02d}.mp3"

            output_file = await self.convert_article(article, filename)
            if output_file:
                output_files.append(output_file)

            # 显示进度
            logger.info(f"Progress: {i}/{len(articles)}")

        logger.info(f"\n✓ Successfully converted {len(output_files)}/{len(articles)} articles")
        return output_files

    async def convert_daily_digest(
        self,
        processed_dir: str = 'data/processed',
        date: Optional[str] = None
    ) -> List[str]:
        """
        转换每日摘要（所有来源的文章）

        Args:
            processed_dir: 处理后的数据目录
            date: 日期（YYYY-MM-DD），None表示今天

        Returns:
            成功转换的文件路径列表
        """
        if not date:
            from datetime import datetime
            date = datetime.now().strftime('%Y-%m-%d')

        # 查找该日期的所有JSON文件
        processed_path = Path(processed_dir)
        json_files = list(processed_path.glob(f"{date}_*.json"))

        if not json_files:
            logger.warning(f"No articles found for date: {date}")
            return []

        logger.info(f"Found {len(json_files)} source files for {date}")

        # 转换所有文件
        all_output_files = []

        for json_file in json_files:
            output_files = await self.convert_from_json(str(json_file))
            all_output_files.extend(output_files)

        return all_output_files


async def main_async():
    """主函数（异步）"""
    import argparse

    parser = argparse.ArgumentParser(
        description="将新闻文章转换为音频",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:

1. 转换单个JSON文件:
   python tools/news_to_audio.py -f data/processed/2026-02-07_36氪_科技_创业.json

2. 转换单个文件，只转换前3篇:
   python tools/news_to_audio.py -f data/processed/2026-02-07_36氪_科技_创业.json -n 3

3. 转换今天的所有文章:
   python tools/news_to_audio.py --daily

4. 转换指定日期的所有文章:
   python tools/news_to_audio.py --daily -d 2026-02-07

5. 使用不同的语音:
   python tools/news_to_audio.py -f file.json --voice yunxi

6. 调整语速:
   python tools/news_to_audio.py -f file.json --rate +20%

可用语音:
  xiaoxiao  - 女声，温柔（默认）
  yunxi     - 男声，沉稳
  yunyang   - 男声，新闻播报
  xiaomo    - 女声，甜美
  yunhao    - 男声，阳光
        """
    )

    parser.add_argument('-f', '--file', help='JSON文件路径')
    parser.add_argument('-n', '--num', type=int, help='最多转换的文章数')
    parser.add_argument('--daily', action='store_true', help='转换每日所有文章')
    parser.add_argument('-d', '--date', help='日期（YYYY-MM-DD）')
    parser.add_argument('--voice', default='xiaoxiao', help='语音名称（默认: xiaoxiao）')
    parser.add_argument('--rate', default='+10%', help='语速（默认: +10%%）')
    parser.add_argument('-o', '--output', default='data/audio', help='输出目录（默认: data/audio）')

    args = parser.parse_args()

    # 创建转换器
    converter = NewsToAudioConverter(
        voice=args.voice,
        rate=args.rate,
        output_dir=args.output
    )

    # 执行转换
    if args.daily:
        # 每日摘要模式
        await converter.convert_daily_digest(date=args.date)

    elif args.file:
        # 单文件模式
        await converter.convert_from_json(args.file, max_articles=args.num)

    else:
        # 没有参数，显示帮助
        parser.print_help()
        print("\n提示: 使用 -f 指定文件，或使用 --daily 转换每日文章")


def main():
    """主函数入口"""
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
