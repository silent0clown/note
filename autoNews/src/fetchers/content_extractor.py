"""
Extract full article content from web pages
"""

import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict, Any
from src.utils.logger import get_logger

logger = get_logger()


class ContentExtractor:
    """Extract full article content from URLs"""

    def __init__(self, timeout: int = 15, user_agent: str = None, session: Optional[requests.Session] = None):
        """
        初始化内容提取器

        Args:
            timeout: 超时时间
            user_agent: User-Agent字符串
            session: 可选的requests.Session对象（用于共享认证、Cookie等）
        """
        self.timeout = timeout

        # 使用提供的session或创建新session
        if session:
            self.session = session
            self.own_session = False  # 标记这不是我们创建的session
        else:
            self.session = requests.Session()
            self.own_session = True
            if user_agent:
                self.session.headers.update({'User-Agent': user_agent})

    def extract(self, url: str) -> Optional[str]:
        """
        Extract full text content from article URL

        Args:
            url: Article URL

        Returns:
            Extracted text content or None if failed
        """
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()

            # Auto detect encoding
            if response.encoding.lower() in ['iso-8859-1', 'windows-1252']:
                response.encoding = response.apparent_encoding

            soup = BeautifulSoup(response.content, 'html.parser')

            # Remove script and style elements
            for script in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
                script.decompose()

            # Try multiple content extraction strategies
            content = None

            # Strategy 1: Common article containers
            article_selectors = [
                'article',
                'div[class*="article"]',
                'div[class*="content"]',
                'div[class*="post"]',
                'div.entry-content',
                'div#content',
                'div.main-content',
                'div[itemprop="articleBody"]',
            ]

            for selector in article_selectors:
                element = soup.select_one(selector)
                if element:
                    content = element.get_text(separator='\n', strip=True)
                    if len(content) > 200:  # Valid content should be substantial
                        logger.debug(f"Extracted content using selector: {selector}")
                        break

            # Strategy 2: Find largest text block (fallback)
            if not content or len(content) < 200:
                paragraphs = soup.find_all('p')
                if paragraphs:
                    content = '\n\n'.join([p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 20])

            # Strategy 3: Full body text (last resort)
            if not content or len(content) < 100:
                body = soup.find('body')
                if body:
                    content = body.get_text(separator='\n', strip=True)

            # Clean up content
            if content:
                # Remove excessive whitespace and merge lines into paragraphs
                lines = [line.strip() for line in content.split('\n') if line.strip()]

                # Filter out very short lines (likely navigation, ads, etc.)
                meaningful_lines = []
                for line in lines:
                    # Skip very short lines unless they are complete sentences
                    if len(line) > 15 or line[-1:] in '。！？.!?':
                        meaningful_lines.append(line)

                # Merge lines into paragraphs
                paragraphs = []
                current_para = []

                for line in meaningful_lines:
                    # Check if line ends with punctuation (paragraph boundary)
                    ends_with_punct = line[-1:] in '。！？.!?；;'

                    current_para.append(line)

                    # If line ends with strong punctuation and is long enough, end paragraph
                    if ends_with_punct and len(line) > 20:
                        # Determine if content is primarily English or Chinese
                        is_english = sum(1 for c in ''.join(current_para) if ord(c) < 128) > len(''.join(current_para)) * 0.5

                        if is_english:
                            para_text = ' '.join(current_para)
                        else:
                            para_text = ''.join(current_para)

                        paragraphs.append(para_text.strip())
                        current_para = []

                # Don't forget the last paragraph
                if current_para:
                    is_english = sum(1 for c in ''.join(current_para) if ord(c) < 128) > len(''.join(current_para)) * 0.5
                    para_text = ' '.join(current_para) if is_english else ''.join(current_para)
                    paragraphs.append(para_text.strip())

                # Join paragraphs with double newline for proper Markdown formatting
                content = '\n\n'.join(paragraphs)

                # Limit length to avoid extremely long articles
                if len(content) > 10000:
                    content = content[:10000] + '...'

                logger.debug(f"Extracted {len(content)} characters from {url[:50]}...")
                return content

            logger.warning(f"Could not extract content from {url}")
            return None

        except requests.Timeout:
            logger.warning(f"Timeout extracting content from {url}")
            return None
        except requests.RequestException as e:
            logger.warning(f"Failed to extract content from {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error extracting content from {url}: {e}")
            return None

    def close(self):
        """Close the session (only if we own it)"""
        if self.own_session and self.session:
            self.session.close()
