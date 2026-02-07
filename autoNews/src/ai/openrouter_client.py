"""
OpenRouter API Client - 使用OpenRouter调用AI模型
"""

import os
from typing import Optional, List, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv
from src.utils.logger import get_logger

logger = get_logger()

# Load environment variables
load_dotenv()


class OpenRouterClient:
    """OpenRouter API 客户端"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        timeout: int = 120
    ):
        """
        初始化OpenRouter客户端

        Args:
            api_key: OpenRouter API Key (如果为None，从环境变量读取)
            model: 模型名称 (如果为None，从环境变量读取)
            timeout: 请求超时时间（秒）
        """
        # 获取API Key
        self.api_key = api_key or os.getenv('OPENROUTER_API_KEY')
        if not self.api_key:
            raise ValueError(
                "OpenRouter API Key not found. "
                "Set OPENROUTER_API_KEY environment variable or pass api_key parameter."
            )

        # 获取模型
        self.model = model or os.getenv('AI_MODEL', 'tngtech/deepseek-r1t2-chimera:free')

        # 初始化OpenAI客户端（OpenRouter兼容OpenAI API）
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
            timeout=timeout
        )

        logger.info(f"OpenRouter client initialized with model: {self.model}")

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """
        调用聊天完成API

        Args:
            messages: 消息列表 [{"role": "user", "content": "..."}]
            temperature: 温度参数 (0-1)
            max_tokens: 最大token数
            **kwargs: 其他参数

        Returns:
            AI响应文本
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )

            content = response.choices[0].message.content
            logger.debug(f"AI response: {content[:100]}...")

            return content

        except Exception as e:
            logger.error(f"OpenRouter API error: {e}")
            raise

    def summarize_text(
        self,
        text: str,
        max_length: int = 500,
        language: str = "中文"
    ) -> str:
        """
        总结文本

        Args:
            text: 要总结的文本
            max_length: 最大字数
            language: 输出语言

        Returns:
            总结文本
        """
        prompt = f"""请用{language}总结以下内容，要求：
1. 提取核心要点
2. 保持客观准确
3. 控制在{max_length}字以内

内容：
{text}

总结："""

        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]

        return self.chat_completion(messages, temperature=0.3)

    def generate_news_digest(
        self,
        articles: List[Dict[str, Any]],
        style: str = "专业",
        max_length: int = 2000
    ) -> str:
        """
        生成新闻摘要稿

        Args:
            articles: 文章列表
            style: 风格（专业/轻松/简洁）
            max_length: 最大字数

        Returns:
            新闻摘要稿
        """
        # 准备文章内容
        articles_text = []
        for i, article in enumerate(articles, 1):
            title = article.get('title', '无标题')
            source = article.get('source', '未知来源')
            content = article.get('content', '') or article.get('summary', '')

            # 限制每篇文章的长度
            if content and len(content) > 500:
                content = content[:500] + "..."

            articles_text.append(f"""
【文章{i}】
标题：{title}
来源：{source}
内容：{content}
""")

        combined_text = "\n".join(articles_text)

        # 构建提示词
        prompt = f"""你是一位资深新闻播音员，请基于以下{len(articles)}篇新闻文章，撰写一份{style}的新闻播报稿。

重要：这是语音播报稿，不是网页文章！请使用纯文本格式。

格式要求（非常重要）：
1. 不要使用任何Markdown符号：禁止使用 #、*、**、-、>、`、[]、() 等符号
2. 不要使用加粗、斜体、标题符号
3. 段落之间用空行分隔
4. 使用"第一"、"第二"或直接用冒号引出要点，例如：
   "开源社区迎来重要更新：KDE Plasma 6.6修复了关键漏洞..."
   或
   "第一，全球科技巨头密集回应AI话题。英伟达CEO黄仁勋表示..."

内容结构：
1. 开场白（150-200字）- 概述今日科技动态
2. 核心要点（7-8条，每条250-350字）- 提炼最重要的新闻，需要详细展开，包含具体数据和细节
3. 趋势分析（200-300字）- 深入总结行业趋势
4. 结束语（100-150字）- 简洁总结

字数要求：必须达到{max_length}字，适合6-7分钟语音播报
重要：请务必写够字数，每条要点要详细展开，不要过于简略

注意事项：
- 务必写完整，不要中途截断
- 不要在文末添加"全文约XX字"或"播报时长XX分钟"
- 就像播音员手中的播报稿一样，直接可读

新闻文章：
{combined_text}

请开始撰写新闻播报稿："""

        messages = [
            {
                "role": "system",
                "content": "你是一位专业的新闻编辑，擅长提炼信息，撰写简洁易懂的新闻摘要。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        logger.info(f"Generating news digest from {len(articles)} articles...")

        return self.chat_completion(
            messages,
            temperature=0.5,
            max_tokens=4000  # 足够生成2000字的中文内容
        )


# 便捷函数
def summarize_articles(
    articles: List[Dict[str, Any]],
    style: str = "专业",
    max_length: int = 1000
) -> str:
    """
    快速总结文章列表

    Args:
        articles: 文章列表
        style: 风格
        max_length: 最大字数

    Returns:
        新闻摘要稿
    """
    client = OpenRouterClient()
    return client.generate_news_digest(articles, style, max_length)
