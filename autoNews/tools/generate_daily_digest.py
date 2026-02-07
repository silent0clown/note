#!/usr/bin/env python3
"""
Daily Digest Generator - 生成每日新闻摘要稿并转换为音频

工作流程：
1. 读取今天所有新闻文章
2. 使用AI总结生成新闻摘要稿
3. 转换为音频
4. 保存文本和音频
"""

import asyncio
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ai import OpenRouterClient
from src.tts import EdgeTTSConverter
from src.utils.logger import setup_logger, get_logger

setup_logger(level="INFO")
logger = get_logger()


class DailyDigestGenerator:
    """每日新闻摘要生成器"""

    def __init__(
        self,
        data_dir: str = 'data/processed',
        output_dir: str = 'data/digest',
        ai_model: Optional[str] = None
    ):
        """
        初始化生成器

        Args:
            data_dir: 处理后的数据目录
            output_dir: 输出目录
            ai_model: AI模型名称
        """
        self.data_dir = Path(data_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # 初始化AI客户端
        self.ai_client = OpenRouterClient(model=ai_model)

        # 初始化TTS转换器
        self.tts_converter = EdgeTTSConverter(
            voice='yunyang',  # 新闻播报使用专业男声
            rate='+10%'       # 稍快语速
        )

    def load_articles_for_date(self, date: str) -> List[Dict[str, Any]]:
        """
        加载指定日期的所有文章

        Args:
            date: 日期（YYYY-MM-DD）

        Returns:
            文章列表
        """
        # 查找该日期的所有JSON文件
        json_files = list(self.data_dir.glob(f"{date}_*.json"))

        if not json_files:
            logger.warning(f"No articles found for date: {date}")
            return []

        logger.info(f"Found {len(json_files)} source files for {date}")

        # 加载所有文章
        all_articles = []
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    articles = json.load(f)
                    all_articles.extend(articles)
                    logger.info(f"Loaded {len(articles)} articles from {json_file.name}")
            except Exception as e:
                logger.error(f"Failed to load {json_file}: {e}")

        return all_articles

    def generate_digest_text(
        self,
        articles: List[Dict[str, Any]],
        style: str = "专业",
        max_length: int = 2000
    ) -> str:
        """
        生成新闻摘要稿文本

        Args:
            articles: 文章列表
            style: 风格
            max_length: 最大字数

        Returns:
            新闻摘要稿
        """
        if not articles:
            return "今天没有新闻。"

        logger.info(f"Generating digest from {len(articles)} articles...")

        # 调用AI生成摘要
        try:
            digest = self.ai_client.generate_news_digest(
                articles,
                style=style,
                max_length=max_length
            )

            logger.info(f"Generated digest: {len(digest)} characters")
            return digest

        except Exception as e:
            logger.error(f"Failed to generate digest: {e}")
            # 降级：使用简单拼接
            return self._fallback_digest(articles)

    def _fallback_digest(self, articles: List[Dict[str, Any]]) -> str:
        """降级方案：简单摘要"""
        parts = ["今日科技要闻：\n"]

        for i, article in enumerate(articles[:10], 1):  # 最多10条
            title = article.get('title', '无标题')
            source = article.get('source', '未知')
            parts.append(f"{i}. {title}（{source}）")

        return "\n".join(parts)

    async def generate_digest_audio(
        self,
        digest_text: str,
        output_file: str
    ) -> bool:
        """
        生成新闻摘要音频

        Args:
            digest_text: 摘要文本
            output_file: 输出文件路径

        Returns:
            是否成功
        """
        logger.info("Converting digest to audio...")

        # 添加开场和结尾
        full_text = f"""
今日新闻摘要

{digest_text}

以上是今天的新闻摘要，感谢收听。
"""

        return await self.tts_converter.convert_text_to_speech(
            full_text,
            output_file
        )

    async def generate_daily_digest(
        self,
        date: Optional[str] = None,
        style: str = "专业",
        max_length: int = 2000,
        generate_audio: bool = True
    ) -> Dict[str, str]:
        """
        生成每日新闻摘要

        Args:
            date: 日期（YYYY-MM-DD），None表示今天
            style: 风格
            max_length: 最大字数
            generate_audio: 是否生成音频

        Returns:
            {"text_file": "...", "audio_file": "..."}
        """
        # 确定日期
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')

        logger.info(f"Generating daily digest for {date}")

        # 加载文章
        articles = self.load_articles_for_date(date)

        if not articles:
            logger.warning("No articles to process")
            return {}

        # 生成摘要文本
        digest_text = self.generate_digest_text(articles, style, max_length)

        # 保存文本
        text_file = self.output_dir / f"{date}_digest.txt"
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write(digest_text)

        logger.info(f"✓ Saved digest text to: {text_file}")

        result = {
            'text_file': str(text_file),
            'digest_text': digest_text
        }

        # 生成音频
        if generate_audio:
            audio_file = self.output_dir / f"{date}_digest.mp3"

            success = await self.generate_digest_audio(
                digest_text,
                str(audio_file)
            )

            if success:
                logger.info(f"✓ Saved digest audio to: {audio_file}")
                result['audio_file'] = str(audio_file)
            else:
                logger.error("Failed to generate audio")

        return result


async def main_async():
    """主函数（异步）"""
    import argparse

    parser = argparse.ArgumentParser(
        description="生成每日新闻摘要稿并转换为音频",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:

1. 生成今天的摘要（文本+音频）:
   python tools/generate_daily_digest.py

2. 生成指定日期的摘要:
   python tools/generate_daily_digest.py -d 2026-02-07

3. 只生成文本，不生成音频:
   python tools/generate_daily_digest.py --no-audio

4. 自定义风格和长度:
   python tools/generate_daily_digest.py --style 轻松 --max-length 800

5. 使用不同的AI模型:
   python tools/generate_daily_digest.py --model meta-llama/llama-3.2-3b-instruct:free

可用风格:
  专业  - 正式、严谨（默认）
  轻松  - 亲切、口语化
  简洁  - 极简、要点式
        """
    )

    parser.add_argument('-d', '--date', help='日期（YYYY-MM-DD）')
    parser.add_argument('--style', default='专业', choices=['专业', '轻松', '简洁'],
                        help='摘要风格（默认: 专业）')
    parser.add_argument('--max-length', type=int, default=2000,
                        help='最大字数（默认: 2000，约5-6分钟播报）')
    parser.add_argument('--no-audio', action='store_true',
                        help='不生成音频')
    parser.add_argument('--model', help='AI模型名称')
    parser.add_argument('-o', '--output', default='data/digest',
                        help='输出目录（默认: data/digest）')

    args = parser.parse_args()

    # 创建生成器
    generator = DailyDigestGenerator(
        output_dir=args.output,
        ai_model=args.model
    )

    # 生成摘要
    result = await generator.generate_daily_digest(
        date=args.date,
        style=args.style,
        max_length=args.max_length,
        generate_audio=not args.no_audio
    )

    if result:
        print("\n" + "="*60)
        print("✅ 每日新闻摘要生成完成！")
        print("="*60)

        if 'text_file' in result:
            print(f"\n📄 文本文件: {result['text_file']}")

        if 'audio_file' in result:
            print(f"🎙️ 音频文件: {result['audio_file']}")

        if 'digest_text' in result:
            print("\n" + "-"*60)
            print("📰 摘要内容预览:")
            print("-"*60)
            preview = result['digest_text'][:500]
            print(preview)
            if len(result['digest_text']) > 500:
                print("...")
            print("-"*60)

        print("\n提示: 使用 --help 查看更多选项")


def main():
    """主函数入口"""
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
